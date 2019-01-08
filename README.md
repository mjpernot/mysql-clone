# Python project for cloning a MySQL database.
# Classification (U)

# Description:
  This program is used to clone a MySQL database either in a replication set or as a standalone database server.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Integration
    - Blackbox


# Features:
  * Clone a MySQL database from another MySQL database.
  * Integrate the clone database into a replication set.
  * Include or remove GTID from the transfer.


# Prerequisites:
  * List of Linux packages that need to be installed on the server.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/cmds_gen
    - lib/arg_parser
    - lib/gen_libs
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

Create MySQL configuration file.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd config
cp mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the MySQL environment.
  * Change these entries in the MySQL setup:
    - passwd = '{ROOT_PASSWORD}'
    - host = '{SERVER_IP}'
    - name = '{HOST_NAME}'
    - sid = {SERVER_ID}
    - extra_def_file = '{Python_Project}/config/mysql.cfg'
  * NOTE:  {SERVER_ID} is the MySQL Server ID.  Run the `select @@server_id;` on the MySQL command line to obtain this value.

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL configuration file:
    - password='{ROOT_PASSWORD}'
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```


# Program Descriptions:
### Program: mysql_clone.py
##### Description: Clone a MySQL database either in a replication set or as a standalone database server.


# Program Help Function:

 The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command: 
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-clone/mysql_clone.py -h
```


# Help Message:
  Below is the help message for the program the program.  Run the program with the -h option get the latest help message for the program.

    Program:  mysql_clone.py

    Description:  The program can clone a database.  The new database can either
        be a standalone copy of the original database or the program
        can integrate the new database into replication with the
        original database creating a master-slave replication setup.

    Usage:
        mysql_clone.py -c source_file -t clone_file -d path
            [-n | -p path | -r] [-v | -h]

    Arguments:
        -c file => Source/Master configuration file.  Required arg.
        -t file => Clone/Slave configuration file.  Required arg.
        -d dir path => Directory path to config files.  Required arg.
        -n => No replication, create a clone of the source database.
        -r => Remove GTID entries from dump file.
        -p dir path => Directory path to mysql programs.  Only required if the
            mysql binary programs do not run properly.  (i.e. not in the $PATH
            variable.)
        -v => Display version of this program.
        -h => Help and usage message.
            NOTE:  -v or -h overrides the other options.

    Notes:
        Source/Master and Clone/Slave config file format (mysql_cfg.py):
            # Configuration file for {Database Name/Server}
            user = "root"
            passwd = "ROOT_PASSWORD"
            # DO NOT USE 127.0.0.1 for the master/source, use actual IP.
            host = "IP_ADDRESS"
            serv_os = "Linux" or "Solaris"
            name = "HOSTNAME"
            port = PORT_NUMBER (default of mysql is 3306)
            cfg_file = "DIRECTORY_PATH/my.cnf"
            sid = "SERVER_ID"
            extra_def_file = "DIRECTORY_PATH/mysql.cfg"

        NOTE 1:  Include the cfg_file even if running remotely as the
            file will be used in future releases.
        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the
            defaults-extra-file format.

        configuration modules -> name is runtime dependent as it can be
            used to connect to different databases with different names.

        Defaults Extra File format (filename.cfg):
            [client]
            password="ROOT_PASSWORD"
            socket="DIRECTORY_PATH/mysql.sock"

        NOTE:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.

    Example:
        mysql_clone.py -c source -t target -d config -n


# Testing:

# Unit Testing:

### Description: Testing consists of unit testing for the functions in the mysql_clone.py program.

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


# Unit test runs for mysql_clone.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-clone
```

### Unit:  help_message

```
test/unit/mysql_clone/help_message.py
```

### Unit:  

```
test/unit/mysql_clone/
```

### Unit:  

```
test/unit/mysql_clone/
```

### Unit:  run_program

```
test/unit/mysql_clone/run_program.py
```

### Unit:  main

```
test/unit/mysql_clone/main.py
```

### All unit testing

```
test/unit/mysql_clone/unit_test_run.sh
```

### Code coverage program

```
test/unit/mysql_clone/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the mysql_clone.py program.

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

### Configuration:

Create MySQL configuration file.

```
cd test/integration/mysql_clone/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the MySQL environment.
  * Change these entries in the MySQL setup.
    - passwd = '{ROOT_PASSWORD}'
    - host = '{SERVER_IP}'
    - name = '{HOST_NAME}'
    - sid = {SERVER_ID}
    - extra_def_file = '{Python_Project}/config/mysql.cfg'
  * NOTE:  {SERVER_ID} is the MySQL Server ID.  Run the `select @@server_id;` on the MySQL command line to obtain this value.

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL setup:
    - password='{ROOT_PASSWORD}'
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```


# Integration test runs for mysql_clone.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-clone
```

### Integration:  

```
test/integration/mysql_clone/

```

### All integration testing

```
test/integration/mysql_clone/integration_test_run.sh
```

### Code coverage program

```
test/integration/mysql_clone/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the mysql_clone.py program.

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

### Configuration:

Create MySQL configuration file.

```
cd test/blackbox/mysql_clone/config
cp ../../../../config/mysql_cfg.py.TEMPLATE mysql_cfg.py
```

Make the appropriate change to the MySQL environment.
  * Change these entries in the MySQL setup:
    - passwd = '{ROOT_PASSWORD}'
    - host = '{SERVER_IP}'
    - name = '{HOST_NAME}'
    - sid = {SERVER_ID}
    - extra_def_file = '{Python_Project}/config/mysql.cfg'
  * NOTE:  {SERVER_ID} is the MySQL Server ID.  Run the `select @@server_id;` on the MySQL command line to obtain this value.

```
vim mysql_cfg.py
chmod 600 mysql_cfg.py
```

Create MySQL definition file.

```
cp ../../../../config/mysql.cfg.TEMPLATE mysql.cfg
```

Make the appropriate change to the MySQL definition setup.
  * Change these entries in the MySQL setup:
    - password='{ROOT_PASSWORD}'
    - socket={BASE_DIR}/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```

# Blackbox test run for mysql_clone.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/mysql-clone
```

### Blackbox:  

```
test/blackbox/mysql_clone/blackbox_test.sh
```

