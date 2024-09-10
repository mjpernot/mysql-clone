# Python project for cloning a MySQL database.
# Classification (U)

# Description:
  Used to clone a MySQL database to a standalone database server or make a slave in a replica set.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Help Function
  * Testing
    - Unit


# Features:
  * Clone a MySQL database from another MySQL database.
  * Integrate the clone database as a slave into a replica set.
  * Include or remove GTID from the transfer.


# Prerequisites:
  * List of Linux packages that need to be installed on the server.
    - Centos 7 (Running Python 2.7):
      -> python-pip
    - Redhat 8 (Running Python 3.6):
      -> python3-pip


# Installation:

Install these programs using git.
  * From here on out, any reference to **{Python_Project}** or **PYTHON_PROJECT** replace with the baseline path of the python program.

```
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-clone.git
```

Install/upgrade system modules.

Centos 7 (Running Python 2.7):
```
sudo pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
NOTE: Install as the user that will run the program.

```
python -m pip install --user -r requirements3.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
```


Install supporting classes and libraries.

Centos 7 (Running Python 2.7):
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

Redhat 8 (Running Python 3.6):
```
python -m pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
python -m pip install -r requirements-mysql-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Configuration:

Create MySQL configuration file for the Master and Slave database.  Make the appropriate change to the MySQL environment.
  * Change these entries in the MySQL setup:
  * NOTE 1:  SERVER_ID is the MySQL Server ID.  Run the `select @@server_id;` on the MySQL command line to obtain this value.
  * NOTE 2:  host:  Do not use 127.0.0.1 for the master IP, use actual IP.
    - user = 'USER'
    - japd = 'PSWORD'
    - rep_user = 'REP_USER'
    - rep_japd = 'REP_PSWORD'
    - host = 'SERVER_IP'
    - name = 'HOST_NAME'
    - sid = SERVER_ID
    - extra_def_file = 'Python_Project/config/mysql_XXXX.cfg'
    - cfg_file = 'DIRECTORY_PATH/my.cnf'

  * These additional entries in the configuration file should not be modified unless necessary.
    - serv_os = 'Linux'
    - port = 3306

  * If SSL connections are being used, configure one or more of these entries:
    - ssl_client_ca = None
    - ssl_client_key = None
    - ssl_client_cert = None

  * Only changes these if necessary and have knowledge in MySQL SSL configuration setup:
    - ssl_client_flag = None
    - ssl_disabled = False
    - ssl_verify_id = False
    - ssl_verify_cert = False

  * TLS version: Set what TLS versions are allowed in the connection set up.
    - tls_versions = []

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg_master.py
cp mysql_cfg.py.TEMPLATE mysql_cfg_slave.py
vim mysql_cfg_master.py
vim mysql_cfg_slave.py
chmod 600 mysql_cfg_master.py mysql_cfg_slave.py
```

Create MySQL definition file for the Master and Slave databases.  Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
  * Note:  socket use is only required to be set in certain conditions when connecting using localhost.
    - password='PSWORD'
    - socket=DIRECTORY_PATH/mysql.sock

```
cp mysql.cfg.TEMPLATE mysql_master.cfg
cp mysql.cfg.TEMPLATE mysql_slave.cfg
vim mysql_master.cfg
vim mysql_slave.cfg
chmod 600 mysql_master.cfg mysql_slave.cfg
```


# Program Help Function:

 The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command: 

```
{Python_Project}/mysql-clone/mysql_clone.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
cd {Python_Project}/mysql-clone
test/unit/mysql_clone/unit_test_run.sh
```

### Code Coverage:

```
cd {Python_Project}/mysql-clone
test/unit/mysql_clone/code_coverage.sh
```

