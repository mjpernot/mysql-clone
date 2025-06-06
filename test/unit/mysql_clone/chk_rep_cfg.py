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
import mysql_clone                              # pylint:disable=E0401,C0413
import version                                  # pylint:disable=E0401,C0413

__version__ = version.__version__


class ArgParser():                                      # pylint:disable=R0903

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
        self.args_array = {}

    def arg_exist(self, arg):

        """Method:  arg_exist

        Description:  Method stub holder for gen_class.ArgParser.arg_exist.

        Arguments:

        """

        return arg in self.args_array


class Server():

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
        test_config_fail_post_8026a
        test_config_fail_post_8026
        test_config_fail_pre_8026a
        test_config_fail_pre_8026
        test_config_faila
        test_config_fail
        test_clone_gtid_off_post_8026a
        test_clone_gtid_off_post_8026
        test_clone_gtid_off_pre_8026a
        test_clone_gtid_off_pre_8026
        test_clone_gtid_offa
        test_clone_gtid_off
        test_config_pass_post_8026a
        test_config_pass_post_8026
        test_config_pass_pre_8026a
        test_config_pass_pre_8026
        test_config_passa
        test_config_pass
        test_mysql_post_8026a
        test_mysql_post_8026
        test_mysql_pre_8026a
        test_mysql_pre_8026
        test_no_rep_post_8026a
        test_no_rep_post_8026
        test_no_rep_pre_8026a
        test_no_rep_pre_8026

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
                "innodb_flush_log_at_trx_commit": "1", "binlog_format": "ROW"},
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
        self.results3 = list(self.opt_arg_list)
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
    def test_config_fail_post_8026a(self, mock_cfg):

        """Function:  test_config_fail_post_8026a

        Description:  Test with configuration checks fails post MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = False
        self.source.version = self.version3

        self.assertFalse(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

    @mock.patch(
        "mysql_clone.mysql_libs.disconnect", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.cfg_chk")
    def test_config_fail_post_8026(self, mock_cfg):

        """Function:  test_config_fail_post_8026

        Description:  Test with configuration checks fails post MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = False
        self.source.version = self.version3

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results3)

    @mock.patch(
        "mysql_clone.mysql_libs.disconnect", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.cfg_chk")
    def test_config_fail_pre_8026a(self, mock_cfg):

        """Function:  test_config_fail_pre_8026a

        Description:  Test with configuration checks fails pre MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = False
        self.source.version = self.version2

        self.assertFalse(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

    @mock.patch(
        "mysql_clone.mysql_libs.disconnect", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.cfg_chk")
    def test_config_fail_pre_8026(self, mock_cfg):

        """Function:  test_config_fail_pre_8026

        Description:  Test with configuration checks fails pre MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = False
        self.source.version = self.version2

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results3)

    @mock.patch(
        "mysql_clone.mysql_libs.disconnect", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.cfg_chk")
    def test_config_faila(self, mock_cfg):

        """Function:  test_config_faila

        Description:  Test with configuration checks fails.

        Arguments:

        """

        mock_cfg.return_value = False
        self.source.version = self.version

        self.assertFalse(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

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

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results3)

    @mock.patch("mysql_clone.cfg_chk")
    def test_clone_gtid_off_post_8026a(self, mock_cfg):

        """Function:  test_clone_gtid_off_post_8026a

        Description:  Test with Clone GTID Mode off post MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version3

        self.clone.gtid_mode = False

        self.assertTrue(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

    @mock.patch("mysql_clone.cfg_chk")
    def test_clone_gtid_off_post_8026(self, mock_cfg):

        """Function:  test_clone_gtid_off_post_8026

        Description:  Test with Clone GTID Mode off post MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version3

        self.clone.gtid_mode = False

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results5)

    @mock.patch("mysql_clone.cfg_chk")
    def test_clone_gtid_off_pre_8026a(self, mock_cfg):

        """Function:  test_clone_gtid_off_pre_8026a

        Description:  Test with Clone GTID Mode off pre MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version2

        self.clone.gtid_mode = False

        self.assertTrue(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

    @mock.patch("mysql_clone.cfg_chk")
    def test_clone_gtid_off_pre_8026(self, mock_cfg):

        """Function:  test_clone_gtid_off_pre_8026

        Description:  Test with Clone GTID Mode off pre MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version2

        self.clone.gtid_mode = False

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results2)

    @mock.patch("mysql_clone.cfg_chk")
    def test_clone_gtid_offa(self, mock_cfg):

        """Function:  test_clone_gtid_offa

        Description:  Test with Clone GTID Mode off.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version

        self.clone.gtid_mode = False

        self.assertTrue(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

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
                self.opt_arg_list)[0], self.results2)

    @mock.patch("mysql_clone.cfg_chk")
    def test_config_pass_post_8026a(self, mock_cfg):

        """Function:  test_config_pass_post_8026a

        Description:  Test with configuration checks pass post MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version3

        self.assertTrue(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

    @mock.patch("mysql_clone.cfg_chk")
    def test_config_pass_post_8026(self, mock_cfg):

        """Function:  test_config_pass_post_8026

        Description:  Test with configuration checks pass post MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version3

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results4)

    @mock.patch("mysql_clone.cfg_chk")
    def test_config_pass_pre_8026a(self, mock_cfg):

        """Function:  test_config_pass_pre_8026a

        Description:  Test with configuration checks pass pre MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version2

        self.assertTrue(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

    @mock.patch("mysql_clone.cfg_chk")
    def test_config_pass_pre_8026(self, mock_cfg):

        """Function:  test_config_pass_pre_8026

        Description:  Test with configuration checks pass pre MySQL 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version2

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results)

    @mock.patch("mysql_clone.cfg_chk")
    def test_config_passa(self, mock_cfg):

        """Function:  test_config_passa

        Description:  Test with configuration checks pass.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version

        self.assertTrue(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

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
                self.opt_arg_list)[0], self.results)

    @mock.patch("mysql_clone.cfg_chk")
    def test_mysql_post_8026a(self, mock_cfg):

        """Function:  test_mysql_post_8026a

        Description:  Test with MySQL 8.0 version post 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version3

        self.assertTrue(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

    @mock.patch("mysql_clone.cfg_chk")
    def test_mysql_post_8026(self, mock_cfg):

        """Function:  test_mysql_post_8026

        Description:  Test with MySQL 8.0 version post 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version3

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results4)

    @mock.patch("mysql_clone.cfg_chk")
    def test_mysql_pre_8026a(self, mock_cfg):

        """Function:  test_mysql_pre_8026a

        Description:  Test with MySQL 8.0 version pre 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version2

        self.assertTrue(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[1])

    @mock.patch("mysql_clone.cfg_chk")
    def test_mysql_pre_8026(self, mock_cfg):

        """Function:  test_mysql_pre_8026

        Description:  Test with MySQL 8.0 version pre 8.0.26.

        Arguments:

        """

        mock_cfg.return_value = True
        self.source.version = self.version2

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results)

    def test_no_rep_post_8026a(self):

        """Function:  test_no_rep_post_8026a

        Description:  Test with no replication configured post MySQL 8.0.26.

        Arguments:

        """

        self.source.version = self.version3

        self.assertTrue(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args2, self.req_rep_cfg,
                self.opt_arg_list)[1])

    def test_no_rep_post_8026(self):

        """Function:  test_no_rep_post_8026

        Description:  Test with no replication configured post MySQL 8.0.26.

        Arguments:

        """

        self.source.version = self.version3

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args2, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results4)

    def test_no_rep_pre_8026a(self):

        """Function:  test_no_rep_pre_8026a

        Description:  Test with no replication configured pre MySQL 8.0.26.

        Arguments:

        """

        self.source.version = self.version2

        self.assertTrue(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args2, self.req_rep_cfg,
                self.opt_arg_list)[1])

    def test_no_rep_pre_8026(self):

        """Function:  test_no_rep_pre_8026

        Description:  Test with no replication configured pre MySQL 8.0.26.

        Arguments:

        """

        self.source.version = self.version2

        self.assertEqual(
            mysql_clone.chk_rep_cfg(
                self.source, self.clone, self.args2, self.req_rep_cfg,
                self.opt_arg_list)[0], self.results)


if __name__ == "__main__":
    unittest.main()
