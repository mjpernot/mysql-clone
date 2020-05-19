#!/usr/bin/python
# Classification (U)

"""Program:  cfg_chk.py

    Description:  Unit testing of cfg_chk in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/cfg_chk.py

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
import mysql_clone
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


def fetch_slv_rep_cfg3():

    """Method:  fetch_slv_rep_cfg3

    Description:  Function stub holder for fetch_slv_rep_cfg function.

    Arguments:

    """

    cls_cfg_dict = {"log_bin": "OFF", "read_only": "ON",
                    "log_slave_updates": "ON", "sync_master_info": "1",
                    "sync_relay_log": "1", "sync_relay_log_info": "1"}

    return cls_cfg_dict


def fetch_slv_rep_cfg2():

    """Method:  fetch_slv_rep_cfg2

    Description:  Function stub holder for fetch_slv_rep_cfg function.

    Arguments:

    """

    cls_cfg_dict = {"log_bin": "ON", "read_only": "OFF",
                    "log_slave_updates": "ON", "sync_master_info": "1",
                    "sync_relay_log": "1", "sync_relay_log_info": "1"}

    return cls_cfg_dict


def fetch_slv_rep_cfg():

    """Method:  fetch_slv_rep_cfg

    Description:  Function stub holder for fetch_slv_rep_cfg function.

    Arguments:

    """

    cls_cfg_dict = {"log_bin": "ON", "read_only": "ON",
                    "log_slave_updates": "ON", "sync_master_info": "1",
                    "sync_relay_log": "1", "sync_relay_log_info": "1"}

    return cls_cfg_dict


def fetch_mst_rep_cfg2():

    """Method:  fetch_mst_rep_cfg2

    Description:  Function stub holder for fetch_mst_rep_cfg function.

    Arguments:

    """

    cls_cfg_dict = {"log_bin": "ON", "sync_binlog": "1",
                    "innodb_flush_log_at_trx_commit": "1",
                    "innodb_support_xa": "ON"}

    return cls_cfg_dict


def fetch_mst_rep_cfg():

    """Method:  fetch_mst_rep_cfg

    Description:  Function stub holder for fetch_mst_rep_cfg function.

    Arguments:

    """

    cls_cfg_dict = {"log_bin": "ON", "sync_binlog": "1",
                    "innodb_flush_log_at_trx_commit": "1",
                    "innodb_support_xa": "ON", "binlog_format": "ROW"}

    return cls_cfg_dict


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_readonly -> Test with no read_only configuration setting.
        test_slave -> Test with slave configuration.
        test_missing_config -> Test with missing configuration options.
        test_master -> Test with master configuration.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

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

    def test_other_error(self):

        """Function:  test_other_error

        Description:  Test with other error then read-only.

        Arguments:

        """

        func_call = fetch_slv_rep_cfg3

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.cfg_chk(func_call,
                                                 self.req_rep_cfg["slave"]))

    def test_no_readonly(self):

        """Function:  test_no_readonly

        Description:  Test with no read_only configuration setting.

        Arguments:

        """

        func_call = fetch_slv_rep_cfg2

        with gen_libs.no_std_out():
            self.assertTrue(mysql_clone.cfg_chk(func_call,
                                                self.req_rep_cfg["slave"]))

    def test_slave(self):

        """Function:  test_slave

        Description:  Test with slave configuration.

        Arguments:

        """

        func_call = fetch_slv_rep_cfg

        self.assertTrue(mysql_clone.cfg_chk(func_call,
                                            self.req_rep_cfg["slave"]))

    def test_missing_config(self):

        """Function:  test_missing_config

        Description:  Test with missing configuration options.

        Arguments:

        """

        func_call = fetch_mst_rep_cfg2

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.cfg_chk(func_call,
                                                 self.req_rep_cfg["master"]))

    def test_master(self):

        """Function:  test_master

        Description:  Test with master configuration.

        Arguments:

        """

        func_call = fetch_mst_rep_cfg

        self.assertTrue(mysql_clone.cfg_chk(func_call,
                                            self.req_rep_cfg["master"]))


if __name__ == "__main__":
    unittest.main()
