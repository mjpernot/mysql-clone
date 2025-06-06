# Classification (U)

"""Program:  crt_dump_cmd.py

    Description:  Unit testing of crt_dump_cmd in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/crt_dump_cmd.py

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
        arg_set_path

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.cmdline = None
        self.args_array = {}

    def arg_set_path(self, arg_opt, **kwargs):

        """Method:  arg_set_path

        Description:  Method stub holder for gen_class.ArgParser.arg_set_path.

        Arguments:

        """

        return os.path.join(
            self.args_array[arg_opt] if arg_opt in self.args_array else "",
            kwargs.get("cmd", ""))


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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_no_opt_arg_list
        test_create_cmd

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.args = ArgParser()
        self.opt_arg_list = ["--single-transaction", "--all-databases",
                             "--triggers", "--routines", "--events",
                             "--ignore-table=mysql.event"]
        self.opt_dump_list = {"-r": "--set-gtid-purged=OFF"}

    @mock.patch("mysql_clone.gen_libs.is_add_cmd")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    def test_no_opt_arg_list(self, mock_cmd, mock_is_add):

        """Function:  test_no_opt_arg_list

        Description:  Test with empty test_no_opt_arg_list list.

        Arguments:

        """

        mock_cmd.return_value = ["command"]
        mock_is_add.return_value = ["command", "arg2"]

        self.assertEqual(
            mysql_clone.crt_dump_cmd(
                self.server, self.args, [], self.opt_dump_list),
            ["command", "arg2"])

    @mock.patch("mysql_clone.gen_libs.is_add_cmd")
    @mock.patch("mysql_clone.gen_libs.add_cmd")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    def test_create_cmd(self, mock_cmd, mock_add, mock_is_add):

        """Function:  test_create_cmd

        Description:  Test with creating command.

        Arguments:

        """

        mock_cmd.return_value = ["command"]
        mock_add.return_value = ["command", "arg1"]
        mock_is_add.return_value = ["command", "arg1", "arg2"]

        self.assertEqual(
            mysql_clone.crt_dump_cmd(
                self.server, self.args, self.opt_arg_list, self.opt_dump_list),
            ["command", "arg1", "arg2"])


if __name__ == "__main__":
    unittest.main()
