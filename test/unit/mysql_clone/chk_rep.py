#!/usr/bin/python
# Classification (U)

"""Program:  chk_rep.py

    Description:  Unit testing of chk_rep in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/chk_rep.py

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
import version

__version__ = version.__version__


class Slave(object):

    """Class:  Slave

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.
        start_slave -> start_slave function.
        upd_slv_status -> upd_slv_status function.
        connect -> connection function.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        pass

    def start_slave(self):

        """Method:  start_slave

        Description:  start_slave function.

        Arguments:

        """

        return True

    def upd_slv_status(self):

        """Method:  upd_slv_status

        Description:  upd_slv_status function.

        Arguments:

        """

        return True

    def connect(self):

        """Method:  connect

        Description:  connect function.

        Arguments:

        """

        return True


class Master(object):

    """Class:  Master

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.
        upd_mst_status -> upd_mst_status function.
        connect -> connection function.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        pass

    def upd_mst_status(self):

        """Method:  upd_mst_status

        Description:  upd_mst_status function.

        Arguments:

        """

        return True

    def connect(self):

        """Method:  connect

        Description:  connect function.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_with_replication -> Test with replication.
        test_no_replication -> Test with no replication.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = Master()
        self.slave = Slave()
        self.clone = Slave()
        self.args_array = {"-c": "mysql_cfg", "-d": "config",
                           "-t": "mysql_cfg2"}
        self.args_array2 = {"-n": True}

    @mock.patch("mysql_clone.cmds_gen.disconnect")
    @mock.patch("mysql_clone.chk_mst_log")
    @mock.patch("mysql_clone.chk_slv_thr")
    @mock.patch("mysql_clone.chk_slv_err")
    @mock.patch("mysql_clone.mysql_libs.change_master_to")
    @mock.patch("mysql_clone.mysql_libs.create_instance")
    def test_with_replication(self, mock_inst, mock_chg, mock_err, mock_thr,
                              mock_log, mock_disc):

        """Function:  test_with_replication

        Description:  Test with replication.

        Arguments:

        """

        mock_inst.side_effect = [self.master, self.slave]
        mock_chg.return_value = True
        mock_err.return_value = True
        mock_thr.return_value = True
        mock_log.return_value = True
        mock_disc.return_value = True

        self.assertFalse(mysql_clone.chk_rep(self.clone, self.args_array))

    def test_no_replication(self):

        """Function:  test_no_replication

        Description:  Test with no replication.

        Arguments:

        """

        self.assertFalse(mysql_clone.chk_rep(self.clone, self.args_array2))


if __name__ == "__main__":
    unittest.main()
