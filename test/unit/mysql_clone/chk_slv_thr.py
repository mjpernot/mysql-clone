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
import unittest
import mock

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
        get_thr_stat
        get_name

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
        setUp
        test_all_good
        test_sql_false
        test_io_false
        test_run_false
        test_thr_down
        test_no_slave

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
