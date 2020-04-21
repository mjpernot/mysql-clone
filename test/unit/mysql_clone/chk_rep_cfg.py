#!/usr/bin/python
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


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.
        upd_mst_rep_stat -> upd_mst_rep_stat function.
        upd_slv_rep_stat -> upd_slv_rep_stat function.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.gtid_mode = True
        self.fetch_mst_rep_cfg = True
        self.fetch_slv_rep_cfg = True

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
        setUp -> Initialize testing environment.
        test_gtid_false -> Test with gtid_mode set to False.
        test_config_pass -> Test with configuration checks pass.
        test_no_rep -> Test with no replication configured.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.source = Server()
        self.clone = Server()
        self.args_array = {}
        self.args_array2 = {"-n": True}
        self.req_rep_cfg = {"master": {"log_bin": "ON",
                                       "sync_binlog": "1",
                                       "innodb_flush_log_at_trx_commit": "1",
                                       "innodb_support_xa": "ON",
                                       "binlog_format": "ROW"},
                            "slave": {"log_bin": "ON",
                                      "read_only": "ON",
                                      "log_slave_updates": "ON",
                                      "sync_master_info": "1",
                                      "sync_relay_log": "1",
                                      "sync_relay_log_info": "1"}}
        self.opt_arg_list = ["--single-transaction", "--all-databases",
                             "--triggers", "--routines", "--events",
                             "--ignore-table=mysql.event"]
        self.results = self.opt_arg_list
        self.results.append("--master-data=2")
        self.results2 = self.opt_arg_list
        self.results2.append("--master-data=1")


    @mock.patch("mysql_clone.cfg_chk")
    def test_gtid_false(self, mock_cfg):

        """Function:  test_gtid_false

        Description:  Test with gtid_mode set to False.

        Arguments:

        """

        self.clone.gtid_mode = False
        mock_cfg.return_value = True

        self.assertEqual(mysql_clone.chk_rep_cfg(
            self.source, self.clone, self.args_array2, self.req_rep_cfg,
            self.opt_arg_list), self.results2)

    @mock.patch("mysql_clone.cfg_chk")
    def test_config_pass(self, mock_cfg):

        """Function:  test_config_pass

        Description:  Test with configuration checks pass.

        Arguments:

        """

        mock_cfg.return_value = True

        self.assertEqual(mysql_clone.chk_rep_cfg(
            self.source, self.clone, self.args_array2, self.req_rep_cfg,
            self.opt_arg_list), self.results)

    def test_no_rep(self):

        """Function:  test_no_rep

        Description:  Test with no replication configured.

        Arguments:

        """

        self.assertEqual(mysql_clone.chk_rep_cfg(
            self.source, self.clone, self.args_array2, self.req_rep_cfg,
            self.opt_arg_list), self.results)


if __name__ == "__main__":
    unittest.main()
