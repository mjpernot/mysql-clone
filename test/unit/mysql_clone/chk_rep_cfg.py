# Classification (U)

"""Program:  chk_rep_cfg.py

    Description:  Unit testing of chk_rep_cfg in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/chk_rep_cfg.py

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
import mysql_clone
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class ArgParser(object):

    """Class:  ArgParser

    Description:  Class stub holder for gen_class.ArgParser class.

    Methods:
        __init__
        arg_exist

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = dict()

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return True if arg in self.args_array else False


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        upd_mst_rep_stat
        upd_slv_rep_stat

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.gtid_mode = True
        self.fetch_mst_rep_cfg = True
        self.fetch_slv_rep_cfg = True
        self.version = None

    def upd_mst_rep_stat(self):

        """Method:  upd_mst_rep_stat

        Description:  upd_mst_rep_stat function.

        Arguments:

        """

        return True

    def upd_slv_rep_stat(self):

        """Method:  upd_slv_rep_stat

        Description:  upd_slv_rep_stat function.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_config_fail3
        test_config_fail2
        test_config_fail
        test_clone_gtid_off3
        test_clone_gtid_off2
        test_clone_gtid_off
        test_config_pass3
        test_config_pass2
        test_config_pass
        test_mysql_80a
        test_mysql_80
        test_no_rep2
        test_no_rep

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.source = Server()
        self.clone = Server()
        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args.args_array = {}
        self.args2.args_array = {"-n": True}
        self.req_rep_cfg = {
            "master": {
                "log_bin": "ON", "sync_binlog": "1",
                "innodb_flush_log_at_trx_commit": "1",
                "innodb_support_xa": "ON", "binlog_format": "ROW"},
            "slave": {
                "log_bin": "ON", "read_only": "ON", "log_slave_updates": "ON",
                "sync_master_info": "1", "sync_relay_log": "1",
                "sync_relay_log_info": "1"}}
        self.opt_arg_list = [
            "--single-transaction", "--all-databases", "--triggers",
            "--routines", "--events", "--ignore-table=mysql.event"]
        self.results = list(self.opt_arg_list)
        self.results.append("--master-data=2")
        self.results2 = list(self.opt_arg_list)
        self.results2.append("--master-data=1")
        self.results3 = list()
        self.results4 = list(self.opt_arg_list)
        self.results4.append("--source-data=2")
        self.results5 = list(self.opt_arg_list)
        self.results5.append("--source-data=1")
        self.version = (5, 7)
        self.version2 = (8, 0, 24)
        self.version3 = (8, 0, 28)

    @mock.patch(
        "mysql_clone.mysql_libs.disconnect", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.cfg_chk")
    def test_config_fail3(self, mock_cfg):

        """Function:  test_config_fail3

        Description:  Test with configuration checks fails post MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = False
        self.source.version = self.version3

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_clone.chk_rep_cfg(
                    self.source, self.clone, self.args, self.req_rep_cfg,
                    self.opt_arg_list), self.results3)

    @mock.patch(
        "mysql_clone.mysql_libs.disconnect", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.cfg_chk")
    def test_config_fail2(self, mock_cfg):

        """Function:  test_config_fail2

        Description:  Test with configuration checks fails pre MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = False
        self.source.version = self.version2

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_clone.chk_rep_cfg(
                    self.source, self.clone, self.args, self.req_rep_cfg,
                    self.opt_arg_list), self.results3)

    @mock.patch(
        "mysql_clone.mysql_libs.disconnect", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.cfg_chk")
    def test_config_fail(self, mock_cfg):

        """Function:  test_config_fail

        Description:  Test with configuration checks fails.

        Arguments:

        """

        mock_cfg.return_value = False
        self.source.version = self.version

        with gen_libs.no_std_out():
            self.assertEqual(
                mysql_clone.chk_rep_cfg(
                    self.source, self.clone, self.args, self.req_rep_cfg,
                    self.opt_arg_list), self.results3)

    @mock.patch("mysql_clone.cfg_chk")
    def test_clone_gtid_off3(self, mock_cfg):

        """Function:  test_clone_gtid_off3

        Description:  Test with Clone GTID Mode off post MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version3

        self.clone.gtid_mode = False

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list), self.results5)

    @mock.patch("mysql_clone.cfg_chk")
    def test_clone_gtid_off2(self, mock_cfg):

        """Function:  test_clone_gtid_off2

        Description:  Test with Clone GTID Mode off pre MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version2

        self.clone.gtid_mode = False

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list), self.results2)

    @mock.patch("mysql_clone.cfg_chk")
    def test_clone_gtid_off(self, mock_cfg):

        """Function:  test_clone_gtid_off

        Description:  Test with Clone GTID Mode off.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version

        self.clone.gtid_mode = False

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list), self.results2)

    @mock.patch("mysql_clone.cfg_chk")
    def test_config_pass3(self, mock_cfg):

        """Function:  test_config_pass3

        Description:  Test with configuration checks pass post MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version3

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list), self.results4)

    @mock.patch("mysql_clone.cfg_chk")
    def test_config_pass2(self, mock_cfg):

        """Function:  test_config_pass2

        Description:  Test with configuration checks pass pre MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version2

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list), self.results)

    @mock.patch("mysql_clone.cfg_chk")
    def test_config_pass(self, mock_cfg):

        """Function:  test_config_pass

        Description:  Test with configuration checks pass.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list), self.results)

    @mock.patch("mysql_clone.cfg_chk")
    def test_mysql_80a(self, mock_cfg):

        """Function:  test_mysql_80a

        Description:  Test with MySQL 8.0 version post 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version3

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list), self.results4)

    @mock.patch("mysql_clone.cfg_chk")
    def test_mysql_80(self, mock_cfg):

        """Function:  test_mysql_80

        Description:  Test with MySQL 8.0 version pre 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version2

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list), self.results)

    def test_no_rep2(self):

        """Function:  test_no_rep2

        Description:  Test with no replication configured post MySQL 8.0.26.

        Arguments:

        """

        self.source.version = self.version3

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args2, self.req_rep_cfg,
                self.opt_arg_list), self.results4)

    def test_no_rep(self):

        """Function:  test_no_rep

        Description:  Test with no replication configured pre MySQL 8.0.26.

        Arguments:

        """

        self.source.version = self.version2

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args2, self.req_rep_cfg,
                self.opt_arg_list), self.results)


if __name__ == "__main__":
    unittest.main()
