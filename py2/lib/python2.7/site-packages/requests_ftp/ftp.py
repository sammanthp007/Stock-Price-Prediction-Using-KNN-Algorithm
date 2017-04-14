# -*- encoding: utf-8 -*-
import requests
import ftplib
import base64
from requests.compat import urlparse
from requests.hooks import dispatch_hook
from requests import Response, codes
from io import BytesIO
import cgi
import os
import socket

from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout
from requests.exceptions import RequestException
from requests.utils import prepend_scheme_if_needed

class FTPSession(requests.Session):
    def __init__(self):
        super(FTPSession, self).__init__()
        self.mount('ftp://', FTPAdapter())

    # Define our helper methods.
    def list(self, url, **kwargs):
        '''Sends an FTP LIST. Returns a Response object.'''
        return self.request('LIST', url, **kwargs)

    def retr(self, url, **kwargs):
        '''Sends an FTP RETR for a given url. Returns a Response object whose
        content field contains the binary data.'''
        return self.request('RETR', url, **kwargs)

    def stor(self, url, files=None, **kwargs):
        '''Sends an FTP STOR to a given URL. Returns a Response object. Expects
        to be given one file by the standard Requests method. The remote
        filename will be given by the URL provided.'''
        return self.request('STOR', url, files=files, **kwargs)

    def nlst(self, url, **kwargs):
        '''Sends an FTP NLST. Returns a Response object.'''
        return self.request('NLST', url, **kwargs)

    def size(self, url, **kwargs):
        '''Sends an FTP SIZE. Returns a decimal number.'''
        return self.request('SIZE', url, **kwargs)


def monkeypatch_session():
    '''Monkeypatch Requests Sessions to provide all the helper
    methods needed for use with FTP.'''

    requests.Session = FTPSession
    return


def parse_multipart_files(request):
    '''Given a prepared reqest, return a file-like object containing the
    original data. This is pretty hacky.'''
    # Start by grabbing the pdict.
    _, pdict = cgi.parse_header(request.headers['Content-Type'])

    # Now, wrap the multipart data in a BytesIO buffer. This is annoying.
    buf = BytesIO()
    buf.write(request.body)
    buf.seek(0)

    # Parse the data. Simply take the first file.
    data = cgi.parse_multipart(buf, pdict)
    _, filedata = data.popitem()
    buf.close()

    # Get a BytesIO now, and write the file into it.
    buf = BytesIO()
    buf.write(''.join(filedata))
    buf.seek(0)

    return buf


def data_callback_factory(variable):
    '''Returns a callback suitable for use by the FTP library. This callback
    will repeatedly save data into the variable provided to this function. This
    variable should be a file-like structure.'''
    def callback(data):
        variable.write(data)
        if hasattr(variable, "content_len"):
            variable.content_len += len(data)
        else:
            variable.content_len = len(data)

        return

    return callback


def build_text_response(request, data, code):
    '''Build a response for textual data.'''
    return build_response(request, data, code, 'ascii')


def build_binary_response(request, data, code):
    '''Build a response for data whose encoding is unknown.'''
    return build_response(request, data, code,  None)


def build_response(request, data, code, encoding):
    '''Builds a response object from the data returned by ftplib, using the
    specified encoding.'''
    response = Response()

    response.encoding = encoding

    # Fill in some useful fields.
    response.raw = data
    response.url = request.url
    response.request = request
    response.status_code = int(code.split()[0])
    if hasattr(data, "content_len"):
        response.headers['Content-Length'] = str(data.content_len)

    # Make sure to seek the file-like raw object back to the start.
    response.raw.seek(0)

    # Run the response hook.
    response = dispatch_hook('response', request.hooks, response)
    return response


class FTPAdapter(requests.adapters.BaseAdapter):
    '''A Requests Transport Adapter that handles FTP urls.'''
    def __init__(self):
        super(FTPAdapter, self).__init__()

        # Build a dictionary keyed off the methods we support in upper case.
        # The values of this dictionary should be the functions we use to
        # send the specific queries.
        self.func_table = {'LIST': self.list,
                           'RETR': self.retr,
                           'STOR': self.stor,
                           'NLST': self.nlst,
                           'SIZE': self.size,
                           'HEAD': self.head,
                           'GET': self.get,}

    def send(self, request, **kwargs):
        '''Sends a PreparedRequest object over FTP. Returns a response object.
        '''
        # Get the authentication from the prepared request, if any.
        auth = self.get_username_password_from_header(request)

        # Next, get the host and the path.
        scheme, host, port, path = self.get_host_and_path_from_url(request)

        # Sort out the timeout.
        timeout = kwargs.get('timeout', None)

        # Look for a proxy
        proxies = kwargs.get('proxies', {})
        proxy = proxies.get(scheme)

        # If there is a proxy, then we actually want to make a HTTP request
        if proxy:
            return self.send_proxy(request, proxy, **kwargs)

        # Establish the connection and login if needed.
        self.conn = ftplib.FTP()

        # Use a flag to distinguish read vs connection timeouts, and a flat set
        # of except blocks instead of a nested try-except, because python 3
        # exception chaining makes things weird
        connected = False

        try:
            self.conn.connect(host, port, timeout)
            connected = True

            if auth is not None:
                self.conn.login(auth[0], auth[1])
            else:
                self.conn.login()

            # Get the method and attempt to find the function to call.
            resp = self.func_table[request.method](path, request)
        except socket.timeout as e:
            # requests distinguishes between connection timeouts and others
            if connected:
                raise ReadTimeout(e, request=request)
            else:
                raise ConnectTimeout(e, request=request)
        # ftplib raises EOFError if the connection is unexpectedly closed.
        # Convert that or any other socket error to a ConnectionError.
        except (EOFError, socket.error) as e:
            raise ConnectionError(e, request=request)
        # Raised for 5xx errors. FTP uses 550 for both ENOENT and EPERM type
        # errors, so just translate all of these into a http-ish 404
        except ftplib.error_perm as e:
            # The exception message is probably from the server, so if it's
            # non-ascii, who knows what the encoding is. Latin1 has the
            # advantage of not being able to fail.
            resp = build_text_response(request,
                    BytesIO(str(e).encode('latin1')), str(codes.not_found))
        # 4xx reply, translate to a http 503
        except ftplib.error_temp as e:
            resp = build_text_response(request,
                    BytesIO(str(e).encode('latin1')), str(codes.unavailable))
        # error_reply is an unexpected status code, and error_proto is an
        # invalid status code. Error is the generic ftplib error, usually
        # raised when a line is too long. Translate all of them to a generic
        # RequestException
        except (ftplib.error_reply, ftplib.error_proto, ftplib.Error) as e:
            raise RequestException(e, request=request)

        # Return the response.
        return resp

    def close(self):
        '''Dispose of any internal state.'''
        # Currently this is a no-op.
        pass

    def send_proxy(self, request, proxy, **kwargs):
        '''Send a FTP request through a HTTP proxy'''
        # Direct the request through a HTTP adapter instead
        proxy_url = prepend_scheme_if_needed(proxy, 'http')
        s = requests.Session()
        adapter = s.get_adapter(proxy_url)

        try:
            return adapter.send(request, **kwargs)
        finally:
            adapter.close()

    def list(self, path, request):
        '''Executes the FTP LIST command on the given path.'''
        data = BytesIO()

        # To ensure the BytesIO object gets cleaned up, we need to alias its
        # close method to the release_conn() method. This is a dirty hack, but
        # there you go.
        data.release_conn = data.close

        self.conn.cwd(path)
        code = self.conn.retrbinary('LIST', data_callback_factory(data))

        # When that call has finished executing, we'll have all our data.
        response = build_text_response(request, data, code)

        # Close the connection.
        self.conn.close()

        return response

    def retr(self, path, request):
        '''Executes the FTP RETR command on the given path.'''
        data = BytesIO()

        # To ensure the BytesIO gets cleaned up, we need to alias its close
        # method. See self.list().
        data.release_conn = data.close

        code = self.conn.retrbinary('RETR ' + path, data_callback_factory(data))

        response = build_binary_response(request, data, code)

        # Close the connection.
        self.conn.close()

        return response

    def get(self, path, request):
        '''Executes the FTP RETR command on the given path.

           This is the same as retr except that the FTP server code is
           converted to a HTTP 200.
        '''

        response = self.retr(path, request)

        # Errors are handled in send(), so assume everything is ok if we
        # made it this far
        response.status_code = codes.ok
        return response

    def size(self, path, request):
        '''Executes the FTP SIZE command on the given path.'''
        self.conn.voidcmd('TYPE I')  # SIZE is not usually allowed in ASCII mode

        size = self.conn.size(path)

        if not str(size).isdigit():
            self.conn.close()
            return None

        data = BytesIO(bytes(size))
        # To ensure the BytesIO gets cleaned up, we need to alias its close
        # method to the release_conn() method. This is a dirty hack, but there
        # you go.
        data.release_conn = data.close
        data.content_len = size

        response = build_text_response(request, data, '213')

        self.conn.close()

        return response

    def head(self, path, request):
        '''Executes the FTP SIZE command on the given path.

           This is the same as size except that the FTP server code is
           converted to a HTTP 200.
        '''

        response = self.size(path, request)
        response.status_code = codes.ok
        return response

    def stor(self, path, request):
        '''Executes the FTP STOR command on the given path.'''

        # First, get the file handle. We assume (bravely)
        # that there is only one file to be sent to a given URL. We also
        # assume that the filename is sent as part of the URL, not as part of
        # the files argument. Both of these assumptions are rarely correct,
        # but they are easy.
        data = parse_multipart_files(request)

        # Split into the path and the filename.
        path, filename = os.path.split(path)

        # Switch directories and upload the data.
        self.conn.cwd(path)
        code = self.conn.storbinary('STOR ' + filename, data)

        # Close the connection and build the response.
        self.conn.close()

        response = build_binary_response(request, BytesIO(), code)

        return response

    def nlst(self, path, request):
        '''Executes the FTP NLST command on the given path.'''
        data = BytesIO()

        # Alias the close method.
        data.release_conn = data.close

        self.conn.cwd(path)
        code = self.conn.retrbinary('NLST', data_callback_factory(data))

        # When that call has finished executing, we'll have all our data.
        response = build_text_response(request, data, code)

        # Close the connection.
        self.conn.close()

        return response

    def get_username_password_from_header(self, request):
        '''Given a PreparedRequest object, reverse the process of adding HTTP
        Basic auth to obtain the username and password. Allows the FTP adapter
        to piggyback on the basic auth notation without changing the control
        flow.'''
        auth_header = request.headers.get('Authorization')

        if auth_header:
            # The basic auth header is of the form 'Basic xyz'. We want the
            # second part. Check that we have the right kind of auth though.
            encoded_components = auth_header.split()[:2]
            if encoded_components[0] != 'Basic':
                raise AuthError('Invalid form of Authentication used.')
            else:
                encoded = encoded_components[1]

            # Decode the base64 encoded string.
            decoded = base64.b64decode(encoded)

            # The auth string was encoded to bytes by requests using latin1,
            # and will be encoded to bytes by ftplib (in python 3) using
            # latin1. In the meantime, use a str
            decoded = decoded.decode('latin1')

            # The string is of the form 'username:password'. Split on the
            # colon.
            components = decoded.split(':')
            username = components[0]
            password = components[1]
            return (username, password)
        else:
            # No auth header. Return None.
            return None

    def get_host_and_path_from_url(self, request):
        '''Given a PreparedRequest object, split the URL in such a manner as to
        determine the host and the path. This is a separate method to wrap some
        of urlparse's craziness.'''
        url = request.url
        # scheme, netloc, path, params, query, fragment = urlparse(url)
        parsed = urlparse(url)
        scheme = parsed.scheme
        path = parsed.path

        # If there is a slash on the front of the path, chuck it.
        if path.startswith('/'):
            path = path[1:]

        host = parsed.hostname
        port = parsed.port or 0

        return (scheme, host, port, path)


class AuthError(Exception):
    '''Denotes an error with authentication.'''
    pass
