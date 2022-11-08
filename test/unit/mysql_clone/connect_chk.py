# Classification (U)

"""Program:  connect_chk.py

    Description:  Unit testing of connect_chk in mysql_clone.py.

    Usage:
        test/unit/mysql_clone/connect_chk.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os
import unittest

# Third-party

# Local
sys.path.append(os.getcwd())
import mysql_clone
import version

__version__ = version.__version__


class Server(object):

    """Class:  Server

    Description:  Class stub holder for mysql_class.Server class.

    Methods:
        __init__
        connect
        set_srv_gtid
        is_connected

    """

    def __init__(self):

        """Method:  __init__

        Description:  Class initialization.

        Arguments:

        """

        self.connected = True

    def connect(self):

        """Method:  connect

        Description:  connect method.

        Arguments:

        """

        return True

    def is_connected(self):

        """Method:  is_connected

        Description:  is_connected method.

        Arguments:

        """

        return self.connected


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_not_connected
        test_is_connected

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.server = Server()

    def test_not_connected(self):

        """Function:  test_not_connected

        Description:  Test with server is not connected.

        Arguments:

        """

        self.server.connected = False

        self.assertFalse(mysql_clone.connect_chk(self.server))

    def test_is_connected(self):

        """Function:  test_is_connected

        Description:  Test with server is still connected.

        Arguments:

        """

        self.assertFalse(mysql_clone.connect_chk(self.server))


if __name__ == "__main__":
    unittest.main()
