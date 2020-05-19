#!/usr/bin/python
# Classification (U)

"""Program:  dump_load_dbs.py

    Description:  Unit testing of dump_load_dbs in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/dump_load_dbs.py

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


class Popen(object):

    """Class:  Popen

    Description:  Class stub holder for subprocess.Popen class.

    Methods:
        __init__ -> Class initialization.
        wait -> Wait function.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.stdout = ["binlog1"]

    def wait(self):

        """Method:  wait

        Description:  Wait function.

        Arguments:

        """

        return True


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.gtid_mode = True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_gtid -> Test with -r option in args_array.
        test_add_opt_dump -> Test with adding optional dump list commands.
        test_create_cmd -> Test with creating command.

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
        self.args_array3 = {"-n": True, "-r": True}
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

    @mock.patch("mysql_clone.subprocess.PIPE", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.subprocess.Popen")
    @mock.patch("mysql_clone.mysql_libs.reset_master")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    @mock.patch("mysql_clone.arg_parser.arg_set_path")
    @mock.patch("mysql_clone.crt_dump_cmd")
    def test_no_gtid(self, mock_cmd, mock_path, mock_crtcmd, mock_reset,
                     mock_popen):

        """Function:  test_no_gtid

        Description:  Test with -r option in args_array.

        Arguments:

        """

        self.clone.gtid_mode = False
        mock_cmd.return_value = ["command", "arg1", "arg2"]
        mock_path.return_value = "./"
        mock_crtcmd.return_value = ["command", "arg1"]
        mock_reset.return_value = True
        mock_popen.side_effect = [Popen(), Popen()]

        self.assertFalse(mysql_clone.dump_load_dbs(
            self.source, self.clone, self.args_array2, self.req_rep_cfg,
            self.opt_arg_list))

    @mock.patch("mysql_clone.subprocess.PIPE", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.subprocess.Popen")
    @mock.patch("mysql_clone.mysql_libs.reset_master")
    @mock.patch("mysql_clone.cmds_gen.is_add_cmd")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    @mock.patch("mysql_clone.arg_parser.arg_set_path")
    @mock.patch("mysql_clone.crt_dump_cmd")
    def test_add_opt_dump(self, mock_cmd, mock_path, mock_crtcmd, mock_isadd,
                          mock_reset, mock_popen):

        """Function:  test_add_opt_dump

        Description:  Test with adding optional dump list commands.

        Arguments:

        """

        self.clone.gtid_mode = False
        mock_cmd.return_value = ["command", "arg1", "arg2"]
        mock_path.return_value = "./"
        mock_crtcmd.return_value = ["command", "arg1"]
        mock_isadd.return_value = ["command", "arg1", "arg2"]
        mock_reset.return_value = True
        mock_popen.side_effect = [Popen(), Popen()]

        self.assertFalse(mysql_clone.dump_load_dbs(
            self.source, self.clone, self.args_array2, self.req_rep_cfg,
            self.opt_arg_list))

    @mock.patch("mysql_clone.subprocess.PIPE", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.subprocess.Popen")
    @mock.patch("mysql_clone.mysql_libs.reset_master")
    @mock.patch("mysql_clone.cmds_gen.is_add_cmd")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    @mock.patch("mysql_clone.arg_parser.arg_set_path")
    @mock.patch("mysql_clone.crt_dump_cmd")
    def test_create_cmd(self, mock_cmd, mock_path, mock_crtcmd, mock_isadd,
                        mock_reset, mock_popen):

        """Function:  test_create_cmd

        Description:  Test with creating command.

        Arguments:

        """

        mock_cmd.return_value = ["command", "arg1", "arg2"]
        mock_path.return_value = "./"
        mock_crtcmd.return_value = ["command", "arg1"]
        mock_isadd.return_value = ["command", "arg1", "arg2"]
        mock_reset.return_value = True
        mock_popen.side_effect = [Popen(), Popen()]

        self.assertFalse(mysql_clone.dump_load_dbs(
            self.source, self.clone, self.args_array, self.req_rep_cfg,
            self.opt_arg_list))


if __name__ == "__main__":
    unittest.main()
