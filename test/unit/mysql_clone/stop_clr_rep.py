# Classification (U)

"""Program:  stop_clr_rep.py

    Description:  Unit testing of stop_clr_rep in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/stop_clr_rep.py

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
        setUp
        test_stat_fail
        test_stop_slave

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.clone = Server()
        self.args = ArgParser()
        self.args2 = ArgParser()
        self.args.args_array = {}
        self.args2.args_array = {"-n": True}

    @mock.patch("mysql_clone.mysql_libs.reset_slave",
                mock.Mock(return_value=True))
    @mock.patch("mysql_clone.mysql_class.slave_stop")
    @mock.patch("mysql_clone.mysql_class.show_slave_stat")
    def test_reset_slave(self, mock_stat, mock_stop):

        """Function:  test_reset_slave

        Description:  Test with resetting slave.

        Arguments:

        """

        mock_stat.return_value = True
        mock_stop.return_value = True

        self.assertFalse(
            mysql_clone.stop_clr_rep(self.clone, self.args2))

    @mock.patch("mysql_clone.mysql_class.show_slave_stat")
    def test_stat_fail(self, mock_stat):

        """Function:  test_stat_fail

        Description:  Test with show_slave_stat failing.

        Arguments:

        """

        mock_stat.return_value = False

        self.assertFalse(mysql_clone.stop_clr_rep(self.clone, self.args))

    @mock.patch("mysql_clone.mysql_class.slave_stop")
    @mock.patch("mysql_clone.mysql_class.show_slave_stat")
    def test_stop_slave(self, mock_stat, mock_stop):

        """Function:  test_stop_slave

        Description:  Test with stopping slave.

        Arguments:

        """

        mock_stat.return_value = True
        mock_stop.return_value = True

        self.assertFalse(mysql_clone.stop_clr_rep(self.clone, self.args2))


if __name__ == "__main__":
    unittest.main()
