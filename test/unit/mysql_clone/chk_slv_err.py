#!/usr/bin/python
# Classification (U)

"""Program:  chk_slv_err.py

    Description:  Unit testing of chk_slv_err in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/chk_slv_err.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party

# Local
sys.path.append(os.getcwd())
import mysql_clone
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.
        get_err_stat -> get_err_stat function.
        get_name -> get_name function.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.io_err = "IO"
        self.sql = "SQL"
        self.io_msg = "IO_Messages"
        self.sql_msg = "SQL_Messages"
        self.io_time = "IO_Time"
        self.sql_time = "SQL_Time"
        self.name = "ServerName"

    def get_err_stat(self):

        """Method:  get_err_stat

        Description:  get_err_stat function.

        Arguments:

        """

        return self.io_err, self.sql, self.io_msg, self.sql_msg, \
            self.io_time, self.sql_time

    def get_name(self):

        """Method:  get_name

        Description:  get_name function.

        Arguments:

        """

        return self.name


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_error -> Test with no errors.
        test_sql_error -> Test with SQL error.
        test_io_error -> Test with IO error.
        test_io_sql_errors -> Test with IO and SQL errors.
        test_no_slave -> Test with no slave present.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = Server()
        self.slaves = [self.slave]

    def test_no_error(self):

        """Function:  test_no_error

        Description:  Test with no errors.

        Arguments:

        """

        self.slave.io_err = None
        self.slave.sql = None

        self.assertFalse(mysql_clone.chk_slv_err(self.slaves))

    def test_sql_error(self):

        """Function:  test_sql_error

        Description:  Test with SQL error.

        Arguments:

        """

        self.slave.io_err = None

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv_err(self.slaves))

    def test_io_error(self):

        """Function:  test_io_error

        Description:  Test with IO error.

        Arguments:

        """

        self.slave.sql = None

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv_err(self.slaves))

    def test_io_sql_errors(self):

        """Function:  test_io_sql_errors

        Description:  Test with IO and SQL errors.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv_err(self.slaves))

    def test_no_slave(self):

        """Function:  test_no_slave

        Description:  Test with no slave present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv_err([]))


if __name__ == "__main__":
    unittest.main()
