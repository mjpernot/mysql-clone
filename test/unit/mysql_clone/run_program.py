#!/usr/bin/python
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


class Slave(object):

    """Class:  Slave

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.
        connect -> connect function.
        set_srv_gtid -> set_srv_gtid function.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.gtid_mode = True

    def connect(self):

        """Method:  connect

        Description:  connect function.

        Arguments:

        """

        return True

    def set_srv_gtid(self):

        """Method:  set_srv_gtid

        Description:  set_srv_gtid function.

        Arguments:

        """

        return True


class Master(object):

    """Class:  Master

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.
        connect -> connect function.
        set_srv_gtid -> set_srv_gtid function.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.gtid_mode = True
        self.host = "Server_IP"

    def connect(self):

        """Method:  connect

        Description:  connect function.

        Arguments:

        """

        return True

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
        setUp -> Initialize testing environment.
        test_rep_config_failure -> Test with rep config returning empty list.
        test_master_loop_no_rep -> Test Master Loopback IP with no replication.
        test_master_loop_rep -> Test with Master Loopback IP with replication.
        test_master_ip_rep -> Test with Master IP with replication.
        test_gtid_no_match -> Test with GTID Modes not matching.
        test_status_false -> Test with status set to False.
        test_status_true -> Test with status set to True.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.master = Master()
        self.slave = Slave()
        self.args_array = {"-c": "mysql_cfg", "-d": "config",
                           "-t": "mysql_cfg2"}
        self.args_array2 = {"-c": "mysql_cfg", "-d": "config",
                            "-t": "mysql_cfg2", "-n": True}
        self.opt_arg_list = ["--single-transaction", "--all-databases",
                             "--triggers", "--routines", "--events",
                             "--ignore-table=mysql.event"]
        self.opt_arg_list2 = list()
        self.req_rep_cfg = {"master": {"log_bin": "ON", "sync_binlog": "1",
                                       "innodb_flush_log_at_trx_commit": "1",
                                       "innodb_support_xa": "ON",
                                       "binlog_format": "ROW"},
                            "slave": {"log_bin": "ON", "read_only": "ON",
                                      "log_slave_updates": "ON",
                                      "sync_master_info": "1",
                                      "sync_relay_log": "1",
                                      "sync_relay_log_info": "1"}}

    @mock.patch("mysql_clone.stop_clr_rep", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.chk_rep_cfg")
    @mock.patch("mysql_clone.mysql_libs")
    def test_rep_config_failure(self, mock_lib, mock_cfg):

        """Function:  test_rep_config_failure

        Description:  Test with rep config returning empty list.

        Arguments:

        """

        mock_lib.create_instance.side_effect = [self.master, self.slave]
        mock_lib.is_cfg_valid.return_value = (True, list())
        mock_cfg.return_value = self.opt_arg_list2

        self.assertFalse(mysql_clone.run_program(
            self.args_array, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.cmds_gen.disconnect",
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
        mock_lib.is_cfg_valid.return_value = (True, list())
        mock_cfg.return_value = self.opt_arg_list

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.run_program(
                self.args_array2, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.cmds_gen.disconnect",
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
        mock_lib.is_cfg_valid.return_value = (True, list())
        mock_cfg.return_value = self.opt_arg_list

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.run_program(
                self.args_array, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.cmds_gen.disconnect",
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
        mock_lib.is_cfg_valid.return_value = (True, list())
        mock_cfg.return_value = self.opt_arg_list

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.run_program(
                self.args_array, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.cmds_gen.disconnect",
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
        mock_lib.is_cfg_valid.return_value = (True, list())
        mock_cfg.return_value = self.opt_arg_list

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.run_program(
                self.args_array, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.cmds_gen.disconnect",
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
        mock_cfg.return_value = self.opt_arg_list

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.run_program(
                self.args_array, self.req_rep_cfg, self.opt_arg_list))

    @mock.patch("mysql_clone.cmds_gen.disconnect",
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
        mock_lib.is_cfg_valid.return_value = (True, list())
        mock_cfg.return_value = self.opt_arg_list

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.run_program(
                self.args_array, self.req_rep_cfg, self.opt_arg_list))


if __name__ == "__main__":
    unittest.main()
