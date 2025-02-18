# Classification (U)

"""Program:  chk_mst_log.py

    Description:  Unit testing of chk_mst_log in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/chk_mst_log.py

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


class Slave():

    """Class:  Slave

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        get_log_info
        get_name

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "ServerName"
        self.mst_file = "mst_file"
        self.relay_file = "relay_file"
        self.read_pos = "read_pos"
        self.exec_pos = "exec_pos"

    def get_log_info(self):

        """Method:  get_log_info

        Description:  get_log_info function.

        Arguments:

        """

        return self.mst_file, self.relay_file, self.read_pos, self.exec_pos

    def get_name(self):

        """Method:  get_name

        Description:  get_name function.

        Arguments:

        """

        return self.name


class Master():                                         # pylint:disable=R0903

    """Class:  Master

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        get_log_info

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "ServerName"
        self.fname = "filename"
        self.log_pos = "log_pos"

    def get_log_info(self):

        """Method:  get_log_info

        Description:  get_log_info function.

        Arguments:

        """

        return self.fname, self.log_pos


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_matching
        test_not_matching
        test_slave_only
        test_no_master_slave

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = Master()
        self.slave = Slave()
        self.slaves = [self.slave]

    @mock.patch("mysql_clone.chk_slv", mock.Mock(return_value=True))
    def test_matching(self):

        """Function:  test_matching

        Description:  Test with Master and Slave matching.

        Arguments:

        """

        self.slave.mst_file = "filename"
        self.slave.read_pos = "log_pos"

        self.assertFalse(mysql_clone.chk_mst_log(self.master, self.slaves))

    @mock.patch("mysql_clone.chk_slv", mock.Mock(return_value=True))
    def test_not_matching(self):

        """Function:  test_not_matching

        Description:  Test with Master and Slave not matching.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_mst_log(self.master, self.slaves))

    @mock.patch("mysql_clone.chk_slv", mock.Mock(return_value=True))
    def test_slave_only(self):

        """Function:  test_slave_only

        Description:  Test with slave only.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_mst_log(None, self.slaves))

    def test_no_master_slave(self):

        """Function:  test_no_master_slave

        Description:  Test with no master or slave present.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_mst_log(None, []))


if __name__ == "__main__":
    unittest.main()
