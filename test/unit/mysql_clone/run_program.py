# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/run_program.py

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
        connect
        set_srv_gtid
        is_connected

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.gtid_mode = True
        self.connected = True
        self.conn_msg = None

    def connect(self, silent=False):

        """Method:  connect

        Description:  connect method.

        Arguments:

        """

        status = True

        if silent:
            status = True

        return status

    def set_srv_gtid(self):

        """Method:  set_srv_gtid

        Description:  set_srv_gtid method.

        Arguments:

        """

        return True

    def is_connected(self):

        """Method:  is_connected

        Description:  is_connected method.

        Arguments:

        """

        return self.connected


class Master():

    """Class:  Master

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        connect
        set_srv_gtid

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.gtid_mode = True
        self.host = "Server_IP"
        self.conn_msg = None

    def connect(self, silent=False):

        """Method:  connect

        Description:  connect function.

        Arguments:

        """

        status = True

        if silent:
            status = True

        return status

    def set_srv_gtid(self):

        """Method:  set_srv_gtid

        Description:  set_srv_gtid function.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_both_no_connect
        test_clone_no_connect
        test_source_no_connect
        test_clone_disconnect
        test_rep_config_failure
        test_master_loop_no_rep
        test_master_loop_rep
        test_master_ip_rep
        test_gtid_no_match
        test_status_false
        test_status_true

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = Master()
        self.slave = Slave()
        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args.args_array = {
            "-c": "mysql_cfg", "-d": "config", "-t": "mysql_cfg2"}
        self.args2.args_array = {
            "-c": "mysql_cfg", "-d": "config", "-t": "mysql_cfg2", "-n": True}
        self.opt_arg_list = [
            "--single-transaction", "--all-databases", "--triggers",
            "--routines", "--events", "--ignore-table=mysql.event"]
        self.opt_arg_list2 = []
        self.req_rep_cfg = {
            "master": {
                "log_bin": "ON", "sync_binlog": "1",
                "innodb_flush_log_at_trx_commit": "1",
                "innodb_support_xa": "ON", "binlog_format": "ROW"},
            "slave": {
                "log_bin": "ON", "read_only": "ON", "log_slave_updates": "ON",
                "sync_master_info": "1", "sync_relay_log": "1",
                "sync_relay_log_info": "1"}}

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.mysql_libs")
    def test_both_no_connect(self, mock_lib):

        """Function:  test_both_no_connect

        Description:  Test with not connecting to clone and source.

        Arguments:

        """

        self.master.conn_msg = "Error connecting to master database"
        self.slave.conn_msg = "Error connecting to slave database"

        mock_lib.create_instance.side_effect = [self.master, self.slave]

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.mysql_libs")
    def test_clone_no_connect(self, mock_lib):

        """Function:  test_clone_no_connect

        Description:  Test with not connecting to clone.

        Arguments:

        """

        self.slave.conn_msg = "Error connecting to slave database"

        mock_lib.create_instance.side_effect = [self.master, self.slave]

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.mysql_libs")
    def test_source_no_connect(self, mock_lib):

        """Function:  test_source_no_connect

        Description:  Test with not connecting to source.

        Arguments:

        """

        self.master.conn_msg = "Error connecting to master database"

        mock_lib.create_instance.side_effect = [self.master, self.slave]

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.stop_clr_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.dump_load_dbs", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep_cfg")
    @mock.patch("mysql_clone.mysql_libs")
    def test_clone_disconnect(self, mock_lib, mock_cfg):

        """Function:  test_clone_disconnect

        Description:  Test with clone disconnecting during dump.

        Arguments:

        """

        self.slave.connected = False

        mock_lib.create_instance.side_effect = [self.master, self.slave]
        mock_lib.is_cfg_valid.return_value = (True, [])
        mock_cfg.return_value = (self.opt_arg_list, True)

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.stop_clr_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep_cfg")
    @mock.patch("mysql_clone.mysql_libs")
    def test_rep_config_failure(self, mock_lib, mock_cfg):

        """Function:  test_rep_config_failure

        Description:  Test with rep config returning empty list.

        Arguments:

        """

        mock_lib.create_instance.side_effect = [self.master, self.slave]
        mock_lib.is_cfg_valid.return_value = (True, [])
        mock_cfg.return_value = (self.opt_arg_list2, False)

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.stop_clr_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.dump_load_dbs", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep_cfg")
    @mock.patch("mysql_clone.mysql_libs")
    def test_master_loop_no_rep(self, mock_lib, mock_cfg):

        """Function:  test_master_loop_no_rep

        Description:  Test Master Loopback IP with no replication.

        Arguments:

        """

        self.master.host = "localhost"
        mock_lib.create_instance.side_effect = [self.master, self.slave]
        mock_lib.is_cfg_valid.return_value = (True, [])
        mock_cfg.return_value = (self.opt_arg_list, True)

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args2, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.stop_clr_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.dump_load_dbs", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep_cfg")
    @mock.patch("mysql_clone.mysql_libs")
    def test_master_loop_rep(self, mock_lib, mock_cfg):

        """Function:  test_master_loop_rep

        Description:  Test with Master Loopback IP with replication.

        Arguments:

        """

        self.master.host = "localhost"
        mock_lib.create_instance.side_effect = [self.master, self.slave]
        mock_lib.is_cfg_valid.return_value = (True, [])
        mock_cfg.return_value = (self.opt_arg_list, True)

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.stop_clr_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.dump_load_dbs", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep_cfg")
    @mock.patch("mysql_clone.mysql_libs")
    def test_master_ip_rep(self, mock_lib, mock_cfg):

        """Function:  test_master_ip_rep

        Description:  Test with Master IP with replication.

        Arguments:

        """

        mock_lib.create_instance.side_effect = [self.master, self.slave]
        mock_lib.is_cfg_valid.return_value = (True, [])
        mock_cfg.return_value = (self.opt_arg_list, True)

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.stop_clr_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.dump_load_dbs", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep_cfg")
    @mock.patch("mysql_clone.mysql_libs")
    def test_gtid_no_match(self, mock_lib, mock_cfg):

        """Function:  test_gtid_no_match

        Description:  Test with GTID Modes not matching.

        Arguments:

        """

        self.slave.gtid_mode = False
        mock_lib.create_instance.side_effect = [self.master, self.slave]
        mock_lib.is_cfg_valid.return_value = (True, [])
        mock_cfg.return_value = (self.opt_arg_list, True)

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.stop_clr_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.dump_load_dbs", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep_cfg")
    @mock.patch("mysql_clone.mysql_libs")
    def test_status_false(self, mock_lib, mock_cfg):

        """Function:  test_status_false

        Description:  Test with status set to False.

        Arguments:

        """

        mock_lib.create_instance.side_effect = [self.master, self.slave]
        mock_lib.is_cfg_valid.return_value = (False, ["Error Message"])
        mock_cfg.return_value = (self.opt_arg_list, True)

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.mysql_libs.disconnect",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.stop_clr_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.dump_load_dbs", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep_cfg")
    @mock.patch("mysql_clone.mysql_libs")
    def test_status_true(self, mock_lib, mock_cfg):

        """Function:  test_status_true

        Description:  Test with status set to True.

        Arguments:

        """

        mock_lib.create_instance.side_effect = [self.master, self.slave]
        mock_lib.is_cfg_valid.return_value = (True, [])
        mock_cfg.return_value = (self.opt_arg_list, True)

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.run_program(
                    self.args, self.req_rep_cfg, self.opt_arg_list))


if __name__ == "__main__":
    unittest.main()
