"""
requests_ftp FTP transport adapter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

requests_ftp is a library providing a very stupid transport adapter for use
with the superawesome Python Requests library.

For full documentation, please see the Github repository.

:copyright: (c) 2012 by Cory Benfield
:license: Apache 2.0, see LICENSE for more details.

"""

__title__ = 'requests-ftp'
__version__ = '0.3.1'
__author__ = 'Cory Benfield'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2012 Cory Benfield'

from .ftp import FTPAdapter, monkeypatch_session
