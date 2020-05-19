#!/usr/bin/python
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

        pass


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_opt_arg_list -> Test with empty test_no_opt_arg_list list.
        test_create_cmd -> Test with creating command.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()
        self.args_array = {}
        self.opt_arg_list = ["--single-transaction", "--all-databases",
                             "--triggers", "--routines", "--events",
                             "--ignore-table=mysql.event"]
        self.opt_dump_list = {"-r": "--set-gtid-purged=OFF"}

    @mock.patch("mysql_clone.cmds_gen.is_add_cmd")
    @mock.patch("mysql_clone.arg_parser.arg_set_path")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    def test_no_opt_arg_list(self, mock_cmd, mock_path, mock_is_add):

        """Function:  test_no_opt_arg_list

        Description:  Test with empty test_no_opt_arg_list list.

        Arguments:

        """

        mock_cmd.return_value = ["command"]
        mock_path.return_value = "./"
        mock_is_add.return_value = ["command", "arg2"]

        self.assertEqual(mysql_clone.crt_dump_cmd(self.server, self.args_array,
                                                  [], self.opt_dump_list),
                         ["command", "arg2"])

    @mock.patch("mysql_clone.cmds_gen.is_add_cmd")
    @mock.patch("mysql_clone.cmds_gen.add_cmd")
    @mock.patch("mysql_clone.arg_parser.arg_set_path")
    @mock.patch("mysql_clone.mysql_libs.crt_cmd")
    def test_create_cmd(self, mock_cmd, mock_path, mock_add, mock_is_add):

        """Function:  test_create_cmd

        Description:  Test with creating command.

        Arguments:

        """

        mock_cmd.return_value = ["command"]
        mock_path.return_value = "./"
        mock_add.return_value = ["command", "arg1"]
        mock_is_add.return_value = ["command", "arg1", "arg2"]

        self.assertEqual(mysql_clone.crt_dump_cmd(self.server, self.args_array,
                                                  self.opt_arg_list,
                                                  self.opt_dump_list),
                         ["command", "arg1", "arg2"])


if __name__ == "__main__":
    unittest.main()
