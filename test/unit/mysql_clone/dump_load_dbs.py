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
        arg_exist
        arg_set_path

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

    def arg_set_path(self, arg_opt, **kwargs):

        """Method:  arg_set_path

        Description:  Method stub holder for gen_class.ArgParser.arg_set_path.

        Arguments:

        """

        return os.path.join(
            self.args_array[arg_opt] if arg_opt in self.args_array else "",
            kwargs.get("cmd", ""))


class FileOpen():                                       # pylint:disable=R0903

    """Class:  FileOpen

    Description:  Class stub holder for file open class.

    Methods:
        close

    """

    def close(self):

        """Function:  close

        Description:  Stub holder for close function.

        Arguments:

        """

        return True


class Popen():                                          # pylint:disable=R0903

    """Class:  Popen

    Description:  Class stub holder for subprocess.Popen class.

    Methods:
        __init__
        wait

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


class Server():                                         # pylint:disable=R0903

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__

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
        setUp
        test_err_file
        test_no_err_file
        test_no_gtid
        test_add_opt_dump
        test_create_cmd

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.open = FileOpen()
        self.source = Server()
        self.clone = Server()
        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args3 = ArgParser()
        self.args.args_array = {}
        self.args2.args_array = {"-n": True}
        self.args3.args_array = {"-n": True, "-r": True}
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

    @mock.patch(
        "mysql_clone.gen_libs.is_empty_file", mock.Mock(return_value=False))
    @mock.patch(
        "mysql_clone.gen_libs.crt_file_time", mock.Mock(return_value="Fname"))
    @mock.patch("mysql_clone.subprocess.PIPE", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.open")
    @mock.patch("mysql_clone.subprocess.Popen")
    @mock.patch("mysql_clone.mysql_libs.reset_master")
    @mock.patch("mysql_clone.gen_libs.is_add_cmd")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    @mock.patch("mysql_clone.crt_dump_cmd")
    def test_err_file(                                  # pylint:disable=R0913
            self, mock_cmd, mock_crtcmd, mock_isadd, mock_reset, mock_popen,
            mock_open):

        """Function:  test_err_file

        Description:  Test with error file detected.

        Arguments:

        """

        mock_cmd.return_value = ["command", "arg1", "arg2"]
        mock_crtcmd.return_value = ["command", "arg1"]
        mock_isadd.return_value = ["command", "arg1", "arg2"]
        mock_reset.return_value = True
        mock_popen.side_effect = [Popen(), Popen()]
        mock_open.return_value = self.open

        with gen_libs.no_std_out():
            self.assertFalse(
                mysql_clone.dump_load_dbs(
                    self.source, self.clone, self.args, self.req_rep_cfg,
                    self.opt_arg_list))

    @mock.patch(
        "mysql_clone.gen_libs.is_empty_file", mock.Mock(return_value=True))
    @mock.patch(
        "mysql_clone.gen_libs.crt_file_time", mock.Mock(return_value="Fname"))
    @mock.patch("mysql_clone.subprocess.PIPE", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.open")
    @mock.patch("mysql_clone.subprocess.Popen")
    @mock.patch("mysql_clone.mysql_libs.reset_master")
    @mock.patch("mysql_clone.gen_libs.is_add_cmd")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    @mock.patch("mysql_clone.crt_dump_cmd")
    def test_no_err_file(                               # pylint:disable=R0913
            self, mock_cmd, mock_crtcmd, mock_isadd, mock_reset, mock_popen,
            mock_open):

        """Function:  test_no_err_file

        Description:  Test with no error file detected.

        Arguments:

        """

        mock_cmd.return_value = ["command", "arg1", "arg2"]
        mock_crtcmd.return_value = ["command", "arg1"]
        mock_isadd.return_value = ["command", "arg1", "arg2"]
        mock_reset.return_value = True
        mock_popen.side_effect = [Popen(), Popen()]
        mock_open.return_value = self.open

        self.assertFalse(
            mysql_clone.dump_load_dbs(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list))

    @mock.patch(
        "mysql_clone.gen_libs.is_empty_file", mock.Mock(return_value=True))
    @mock.patch(
        "mysql_clone.gen_libs.crt_file_time", mock.Mock(return_value="Fname"))
    @mock.patch("mysql_clone.subprocess.PIPE", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.open")
    @mock.patch("mysql_clone.subprocess.Popen")
    @mock.patch("mysql_clone.mysql_libs.reset_master")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    @mock.patch("mysql_clone.crt_dump_cmd")
    def test_no_gtid(                                   # pylint:disable=R0913
            self, mock_cmd, mock_crtcmd, mock_reset, mock_popen, mock_open):

        """Function:  test_no_gtid

        Description:  Test with -r option in args_array.

        Arguments:

        """

        self.clone.gtid_mode = False
        mock_cmd.return_value = ["command", "arg1", "arg2"]
        mock_crtcmd.return_value = ["command", "arg1"]
        mock_reset.return_value = True
        mock_popen.side_effect = [Popen(), Popen()]
        mock_open.return_value = self.open

        self.assertFalse(
            mysql_clone.dump_load_dbs(
                self.source, self.clone, self.args2, self.req_rep_cfg,
                self.opt_arg_list))

    @mock.patch(
        "mysql_clone.gen_libs.is_empty_file", mock.Mock(return_value=True))
    @mock.patch(
        "mysql_clone.gen_libs.crt_file_time", mock.Mock(return_value="Fname"))
    @mock.patch("mysql_clone.subprocess.PIPE", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.open")
    @mock.patch("mysql_clone.subprocess.Popen")
    @mock.patch("mysql_clone.mysql_libs.reset_master")
    @mock.patch("mysql_clone.gen_libs.is_add_cmd")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    @mock.patch("mysql_clone.crt_dump_cmd")
    def test_add_opt_dump(                              # pylint:disable=R0913
            self, mock_cmd, mock_crtcmd, mock_isadd, mock_reset, mock_popen,
            mock_open):

        """Function:  test_add_opt_dump

        Description:  Test with adding optional dump list commands.

        Arguments:

        """

        self.clone.gtid_mode = False
        mock_cmd.return_value = ["command", "arg1", "arg2"]
        mock_crtcmd.return_value = ["command", "arg1"]
        mock_isadd.return_value = ["command", "arg1", "arg2"]
        mock_reset.return_value = True
        mock_popen.side_effect = [Popen(), Popen()]
        mock_open.return_value = self.open

        self.assertFalse(
            mysql_clone.dump_load_dbs(
                self.source, self.clone, self.args2, self.req_rep_cfg,
                self.opt_arg_list))

    @mock.patch(
        "mysql_clone.gen_libs.is_empty_file", mock.Mock(return_value=True))
    @mock.patch(
        "mysql_clone.gen_libs.crt_file_time", mock.Mock(return_value="Fname"))
    @mock.patch("mysql_clone.subprocess.PIPE", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.open")
    @mock.patch("mysql_clone.subprocess.Popen")
    @mock.patch("mysql_clone.mysql_libs.reset_master")
    @mock.patch("mysql_clone.gen_libs.is_add_cmd")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    @mock.patch("mysql_clone.crt_dump_cmd")
    def test_create_cmd(                                # pylint:disable=R0913
            self, mock_cmd, mock_crtcmd, mock_isadd, mock_reset, mock_popen,
            mock_open):

        """Function:  test_create_cmd

        Description:  Test with creating command.

        Arguments:

        """

        mock_cmd.return_value = ["command", "arg1", "arg2"]
        mock_crtcmd.return_value = ["command", "arg1"]
        mock_isadd.return_value = ["command", "arg1", "arg2"]
        mock_reset.return_value = True
        mock_popen.side_effect = [Popen(), Popen()]
        mock_open.return_value = self.open

        self.assertFalse(
            mysql_clone.dump_load_dbs(
                self.source, self.clone, self.args, self.req_rep_cfg,
                self.opt_arg_list))


if __name__ == "__main__":
    unittest.main()
