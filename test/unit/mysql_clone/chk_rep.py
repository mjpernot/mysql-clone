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
import unittest
import mock

# Local
sys.path.append(os.getcwd())
import mysql_clone                              # pylint:disable=E0401,C0413
import lib.gen_libs as gen_libs             # pylint:disable=E0401,C0413,R0402
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        get_val
        arg_exist

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {}

    def get_val(self, skey, def_val=None):

        """Method:  get_val

        Description:  Method stub holder for gen_class.ArgParser.get_val.

        Arguments:

        """

        return self.args_array.get(skey, def_val)

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return arg in self.args_array


class Slave():

    """Class:  Slave

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        start_slave
        upd_slv_status
        connect

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.conn_msg = None

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

    def connect(self, silent=False):

        """Method:  connect

        Description:  connect function.

        Arguments:

        """

        status = True

        if silent:
            status = True

        return status


class Master():

    """Class:  Master

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        upd_mst_status
        connect

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.conn_msg = None

    def upd_mst_status(self):

        """Method:  upd_mst_status

        Description:  upd_mst_status function.

        Arguments:

        """

        return True

    def connect(self, silent=False):

        """Method:  connect

        Description:  connect function.

        Arguments:

        """

        status = True

        if silent:
            status = True

        return status


class Cfg():                                            # pylint:disable=R0903

    """Class:  Cfg

    Description:  Stub holder for configuration file.

    Methods:
        __init__

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
        setUp
        test_with_no_slave_connect
        test_with_no_master_connect
        test_with_replication
        test_no_replication

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
        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args.args_array = {
            "-c": "mysql_cfg", "-d": "config", "-t": "mysql_cfg2"}
        self.args2.args_array = {"-n": True}

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.mysql_libs.change_master_to",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.mysql_libs.create_instance")
    def test_with_no_slave_connect(self, mock_inst):

        """Function:  test_with_no_slave_connect

        Description:  Test with failed connection to slave.

        Arguments:

        """

        self.slave.conn_msg = "Error connecting to database"

        mock_inst.side_effect = [self.master, self.slave]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_rep(self.clone, self.args))

    @mock.patch("mysql_clone.mysql_libs.create_instance")
    def test_with_no_master_connect(self, mock_inst):

        """Function:  test_with_no_master_connect

        Description:  Test with failed connection to master.

        Arguments:

        """

        self.master.conn_msg = "Error connecting to database"

        mock_inst.side_effect = [self.master, self.slave]

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.chk_rep(self.clone, self.args))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_mst_log",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_slv_thr",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_slv_err",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.mysql_libs.change_master_to",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.mysql_libs.create_instance")
    def test_with_replication(self, mock_inst):

        """Function:  test_with_replication

        Description:  Test with replication.

        Arguments:

        """

        mock_inst.side_effect = [self.master, self.slave]

        self.assertFalse(mysql_clone.chk_rep(self.clone, self.args))

    def test_no_replication(self):

        """Function:  test_no_replication

        Description:  Test with no replication.

        Arguments:

        """

        self.assertFalse(mysql_clone.chk_rep(self.clone, self.args2))


if __name__ == "__main__":
    unittest.main()
