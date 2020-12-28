#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/main.py

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


class ProgramLock(object):

    """Class:  ProgramLock

    Description:  Class stub holder for gen_class.ProgramLock class.

    Methods:
        __init__ -> Class initialization.

    """

    def __init__(self, cmdline, flavor):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:
            (input) cmdline -> Argv command line.
            (input) flavor -> Lock flavor ID.

        """

        self.cmdline = cmdline
        self.flavor = flavor


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_help_true -> Test help if returns true.
        test_help_false -> Test help if returns false.
        test_cond_req_false -> Test arg_cond_req if returns false.
        test_cond_req_true -> Test arg_cond_req if returns true.
        test_arg_req_true -> Test arg_require if returns true.
        test_arg_req_false -> Test arg_require if returns false.
        test_arg_dir_chk_crt_true -> Test arg_dir_chk_crt if returns True.
        test_arg_dir_chk_crt_false -> Test arg_dir_chk_crt if returns False.
        test_run_program -> Test run_program function.
        test_programlock_true -> Test with ProgramLock returns True.
        test_programlock_false -> Test with ProgramLock returns False.
        test_programlock_id -> Test ProgramLock with flavor ID.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args_array = {"-c": "CfgFile", "-d": "CfgDir"}
        self.args_array2 = {"-c": "CfgFile", "-d": "CfgDir", "-y": "Flavor"}
        self.proglock = ProgramLock(["cmdline"], "FlavorID")

    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser.arg_parse2")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_help_true

        Description:  Test help if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = True

        self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_help_false

        Description:  Test help if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = False

        self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_cond_req_false(self, mock_arg, mock_help):

        """Function:  test_cond_req_false

        Description:  Test arg_cond_req if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = False

        self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_cond_req_true(self, mock_arg, mock_help):

        """Function:  test_cond_req_true

        Description:  Test arg_cond_req if returns true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_require.return_value = True

        self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_arg_req_true(self, mock_arg, mock_help):

        """Function:  test_arg_req_true

        Description:  Test arg_require if returns true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_require.return_value = True

        self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_arg_req_false(self, mock_arg, mock_help):

        """Function:  test_arg_req_false

        Description:  Test arg_require if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_require.return_value = False
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_arg_dir_chk_crt_true(self, mock_arg, mock_help):

        """Function:  test_arg_dir_chk_crt_true

        Description:  Test arg_dir_chk_crt if returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_require.return_value = False
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.run_program")
    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_arg_dir_chk_crt_false(self, mock_arg, mock_help, mock_run):

        """Function:  test_arg_dir_chk_crt_false

        Description:  Test arg_dir_chk_crt if returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_require.return_value = False
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_run.return_value = True

        self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.gen_class.ProgramLock")
    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_run_program(self, mock_arg, mock_help, mock_lock):

        """Function:  test_run_program

        Description:  Test run_program function.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_require.return_value = False
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.gen_class.ProgramLock")
    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_programlock_true(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_true

        Description:  Test with ProgramLock returns True.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_require.return_value = False
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.gen_class.ProgramLock")
    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_programlock_false(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_false

        Description:  Test with ProgramLock returns False.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_require.return_value = False
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_lock.side_effect = \
            mysql_clone.gen_class.SingleInstanceException

        with gen_libs.no_std_out():
            self.assertFalse(mysql_clone.main())

    @mock.patch("mysql_clone.run_program", mock.Mock(return_value=True))
    @mock.patch("mysql_clone.gen_class.ProgramLock")
    @mock.patch("mysql_clone.gen_libs.help_func")
    @mock.patch("mysql_clone.arg_parser")
    def test_programlock_id(self, mock_arg, mock_help, mock_lock):

        """Function:  test_programlock_id

        Description:  Test ProgramLock with flavor ID.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array2
        mock_help.return_value = False
        mock_arg.arg_cond_req.return_value = True
        mock_arg.arg_require.return_value = False
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_lock.return_value = self.proglock

        self.assertFalse(mysql_clone.main())


if __name__ == "__main__":
    unittest.main()
