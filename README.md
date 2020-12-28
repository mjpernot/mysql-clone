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
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/cmds_gen
    - lib/arg_parser
    - lib/gen_libs
    - lib/gen_class
    - mysql_lib/mysql_class
    - mysql_lib/mysql_libs


# Installation:

Install these programs using git.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-clone.git
```

Install/upgrade system modules.

```
cd mysql-clone
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create MySQL configuration file for the Master and Clone/Slave database.  Make the appropriate change to the MySQL environment.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Change these entries in the MySQL setup:
    - user = 'USER'
    - japd = 'PSWORD'
    - rep_user = 'REP_USER'
    - rep_japd = 'REP_PSWORD'
    - host = 'SERVER_IP'
    - name = 'HOST_NAME'
    - sid = SERVER_ID
    - extra_def_file = 'Python_Project/config/mysql_XXXX.cfg'
    - cfg_file = 'DIRECTORY_PATH/my.cnf'
      -> NOTE 1:  SERVER_ID is the MySQL Server ID.  Run the `select @@server_id;` on the MySQL command line to obtain this value.
      -> NOTE 2:  host:  Do not use 127.0.0.1 for the master IP, use actual IP.
      -> NOTE 3:  Change mysql_XXXX.cfg to 'mysql_master.cfg' or 'mysql_slave.cfg' for Master and Slave respectively.
  * These additional entries in the configuration file should not be modified unless necessary.
    - serv_os = 'Linux'
    - port = 3306

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg_master.py
cp mysql_cfg.py.TEMPLATE mysql_cfg_slave.py
vim mysql_cfg_master.py
vim mysql_cfg_slave.py
chmod 600 mysql_cfg_master.py mysql_cfg_slave.py
```

Create MySQL definition file for the Master and Clone/Slave databases.  Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password='PASSWORD'
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
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-clone/mysql_clone.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install these programs using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/mysql-clone.git
```

Install/upgrade system modules.

```
cd mysql-clone
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-mysql-lib.txt --target mysql_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target mysql_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


### Testing:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-clone
test/unit/mysql_clone/unit_test_run.sh
```

### Code Coverage:

```
cd {Python_Project}/mysql-clone
test/unit/mysql_clone/code_coverage.sh
```

