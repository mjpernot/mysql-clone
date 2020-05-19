#!/usr/bin/python
# Classification (U)

"""Program:  chk_slv_thr.py

    Description:  Unit testing of chk_slv_thr in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/chk_slv_thr.py

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
import mock

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
        get_thr_stat -> get_thr_stat function.
        get_name -> get_name function.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.thr = "1"
        self.io_thr = "1"
        self.sql_thr = "1"
        self.run = "1"
        self.name = "ServerName"

    def get_thr_stat(self):

        """Method:  get_thr_stat

        Description:  get_thr_stat function.

        Arguments:

        """

        return self.thr, self.io_thr, self.sql_thr, self.run

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
        test_all_good -> Test with all tests successful.
        test_sql_false -> Test with SQL False.
        test_io_false -> Test with IO False.
        test_run_false -> Test with run False.
        test_thr_down -> Test with thr down.
        test_no_slave -> Test with no slave present.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = Server()
        self.slaves = [self.slave]

    @mock.patch("mysql_clone.gen_libs.is_true")
    def test_all_good(self, mock_is):

        """Function:  test_all_good

        Description:  Test with all tests successful.

        Arguments:

        """

        mock_is.return_value = True

        self.assertFalse(mysql_clone.chk_slv_thr(self.slaves))

    @mock.patch("mysql_clone.gen_libs.is_true")
    def test_sql_false(self, mock_is):

        """Function:  test_sql_false

        Description:  Test with SQL False.

        Arguments:

        """

        mock_is.side_effect = [True, True, False]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv_thr(self.slaves))

    @mock.patch("mysql_clone.gen_libs.is_true")
    def test_io_false(self, mock_is):

        """Function:  test_io_false

        Description:  Test with IO False.

        Arguments:

        """

        mock_is.side_effect = [True, False]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv_thr(self.slaves))

    @mock.patch("mysql_clone.gen_libs.is_true")
    def test_run_false(self, mock_is):

        """Function:  test_run_false

        Description:  Test with run False.

        Arguments:

        """

        mock_is.return_value = False

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv_thr(self.slaves))

    @mock.patch("mysql_clone.gen_libs.is_true")
    def test_thr_down(self, mock_is):

        """Function:  test_thr_down

        Description:  Test with thr down.

        Arguments:

        """

        self.slave.thr = None
        mock_is.return_value = True

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv_thr(self.slaves))

    def test_no_slave(self):

        """Function:  test_no_slave

        Description:  Test with no slave present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv_thr([]))


if __name__ == "__main__":
    unittest.main()
