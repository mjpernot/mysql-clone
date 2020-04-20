# Python project for cloning a MySQL database.
# Classification (U)

# Description:
  This program is used to clone a MySQL database either in a replication set or as a standalone database server.


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
  * Integrate the clone database into a replication set.
  * Include or remove GTID from the transfer.


# Prerequisites:
  * List of Linux packages that need to be installed on the server.
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
    - passwd = 'ROOT_PASSWORD'
    - host = 'SERVER_IP'
    - name = 'HOST_NAME'
    - sid = SERVER_ID
    - extra_def_file = 'Python_Project/config/mysql.cfg'
  * NOTE:  SERVER_ID is the MySQL Server ID.  Run the `select @@server_id;` on the MySQL command line to obtain this value.

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
    - password='ROOT_PASSWORD'
    - socket=BASE_DIR/mysql/tmp/mysql.sock

```
vim mysql.cfg
chmod 600 mysql.cfg
```


# Program Help Function:

 The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command: 
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/mysql-clone/mysql_clone.py -h
```


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

