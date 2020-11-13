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


class Cfg(object):

    """Class:  Cfg

    Description:  Stub holder for configuration file.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.name = "name"
        self.sid = "sid"
        self.user = "user"
        self.japd = None
        self.rep_user = "user"
        self.rep_japd = None
        self.serv_os = "Linux"
        self.host = "hostname"
        self.port = 3306
        self.cfg_file = "cfg_file"
        self.extra_def_file = "extra_def_file"


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
        self.cfg = Cfg()
        self.args_array = {"-c": "mysql_cfg", "-d": "config",
                           "-t": "mysql_cfg2"}
        self.args_array2 = {"-n": True}

    @mock.patch("mysql_clone.cmds_gen.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_mst_log",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_slv_thr",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_slv_err",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.mysql_libs.change_master_to",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.gen_libs.load_module")
    @mock.patch("mysql_clone.mysql_class.MasterRep")
    @mock.patch("mysql_clone.mysql_libs.create_instance")
    def test_with_replication(self, mock_inst, mock_master, mock_load):

        """Function:  test_with_replication

        Description:  Test with replication.

        Arguments:

        """

        mock_inst.return_value = self.slave
        mock_master.return_value = self.master
        mock_load.return_value = self.cfg

        self.assertFalse(mysql_clone.chk_rep(self.clone, self.args_array))

    def test_no_replication(self):

        """Function:  test_no_replication

        Description:  Test with no replication.

        Arguments:

        """

        self.assertFalse(mysql_clone.chk_rep(self.clone, self.args_array2))


if __name__ == "__main__":
    unittest.main()
