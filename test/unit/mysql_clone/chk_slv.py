#!/usr/bin/python
# Classification (U)

"""Program:  chk_slv.py

    Description:  Unit testing of chk_slv in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/chk_slv.py

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
import lib.gen_libs as gen_libs
import mysql_clone
import version

__version__ = version.__version__


class SlaveRep(object):

    """Class:  SlaveRep

    Description:  Class stub holder for mysql_class.SlaveRep class.

    Methods:
        __init__ -> Class initialization.
        get_log_info -> Stub method holder for SlaveRep.get_log_info.
        get_name -> Stub method holder for SlaveRep.get_name.

    """

    def __init__(self, gtid_mode="ON", mst_file="Master_Log",
                 relay_file="Slave_Relay", read_pos=3456, exec_pos=4567):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "Server_Name"
        self.mst_file = mst_file
        self.relay_file = relay_file
        self.read_pos = read_pos
        self.exec_pos = exec_pos
        self.gtid_mode = gtid_mode
        self.retrieved_gtid = 12345678
        self.exe_gtid = 23456789

    def get_log_info(self):

        """Method:  get_log_info

        Description:  Stub method holder for SlaveRep.get_log_info.

        Arguments:

        """

        return self.mst_file, self.relay_file, self.read_pos, self.exec_pos

    def get_name(self):

        """Method:  get_name

        Description:  Stub method holder for SlaveRep.get_name.

        Arguments:

        """

        return self.name


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_delay -> Test with no delays detected.
        test_no_gtid_mode -> Test with Gtid Mode off.
        test_gtid_mode -> Test with Gtid Mode on.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.slave = SlaveRep()

    def test_no_delay(self):

        """Function:  test_no_delay

        Description:  Test with no delays detected.

        Arguments:

        """

        self.slave.mst_file = "Slave_Relay"
        self.slave.read_pos = 4567

        self.assertFalse(mysql_clone.chk_slv(self.slave))

    def test_no_gtid_mode(self):

        """Function:  test_no_gtid_mode

        Description:  Test with Gtid Mode off.

        Arguments:

        """

        self.slave.gtid_mode = False

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv(self.slave))

    def test_gtid_mode(self):

        """Function:  test_gtid_mode

        Description:  Test with Gtid Mode on.

        Arguments:

        """

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_slv(self.slave))


if __name__ == "__main__":
    unittest.main()
