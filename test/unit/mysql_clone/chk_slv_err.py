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
import unittest

# Local
sys.path.append(os.getcwd())
import mysql_clone                              # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class Server():

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        get_err_stat
        get_name

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
        setUp
        test_no_error
        test_sql_error
        test_io_error
        test_io_sql_errors
        test_no_slave

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
