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
        test_with_replication -> Test with replication.

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
        self.opt_arg_list = ["--single-transaction", "--all-databases",
                             "--triggers", "--routines", "--events",
                             "--ignore-table=mysql.event"]
        self.req_rep_cfg = {"master": {"log_bin": "ON", "sync_binlog": "1",
                                       "innodb_flush_log_at_trx_commit": "1",
                                       "innodb_support_xa": "ON",
                                       "binlog_format": "ROW"},
                            "slave": {"log_bin": "ON", "read_only": "ON",
                                      "log_slave_updates": "ON",
                                      "sync_master_info": "1",
                                      "sync_relay_log": "1",
                                      "sync_relay_log_info": "1"}}

    @mock.patch("mysql_clone.cmds_gen.disconnect")
    @mock.patch("mysql_clone.chk_rep")
    @mock.patch("mysql_clone.dump_load_dbs")
    @mock.patch("mysql_clone.chk_rep_cfg")
    @mock.patch("mysql_clone.stop_clr_rep")
    @mock.patch("mysql_clone.mysql_libs")
    def test_status_true(self, mock_lib, mock_clr, mock_cfg, mock_load,
                         mock_chk, mock_disc):

        """Function:  test_with_replication

        Description:  Test with replication.

        Arguments:

        """

        mock_lib.create_instance.side_effect = [self.master, self.slave]
        mock_lib.is_cfg_valid.return_value = (True, None)
        mock_clr.return_value = True
        mock_cfg.return_value = self.opt_arg_list
        mock_load.return_value = True
        mock_chk.return_value = True
        mock_disc.return_value = True

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.run_program(
                self.args_array, self.req_rep_cfg, self.opt_arg_list))


if __name__ == "__main__":
    unittest.main()
