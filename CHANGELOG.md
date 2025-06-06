# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [3.1.0] - 2025-05-30
- Updated python-lib to v4.0.1
- Updated mysql-lib to v5.5.1
- Removed support for MySQL 5.6/5.7

### Changed
- chk_rep: Added in connection status checks for master and slave connections.
- chk_rep_cfg: Added in status return on success of operation and removed print error message and disconnect.
- run_program: Moved disconnect call to each place there is an exit from the function.
- run_program: The chk_rep_cfg also returns a status of the operation and use this status to determine to continue or exit from process.
- run_program: If GTID check fails, disconnect and return from function.
- run_program: Replaced status variable with a disconnect and return from function.
- run_program: Added checks on connection status for source and clone databases.
- chk_rep_cfg: Removed check for innodb_support_xa.
- main: Removed innodb_support_xa from req_rep_cfg dictionary.
- Documentation changes.


## [3.0.0] - 2025-02-18
Breaking Changes

- Removed support for Python 2.7.
- Updated mysql-lib v5.4.0
- Updated python-lib v4.0.0

### Changed
- chk_rep_cfg:  Changed list() to [].
- dump_load_dbs: Added 'encoding' to open() call and changed list() to [].
- Converted strings to f-strings.
- Documentation changes.

### Deprecated
- Support for MySQL 5.6/5.7


## [2.2.6] - 2024-11-19
- Updated python-lib to v3.0.8
- Updated mysql-lib to v5.3.9

### Fixed
- Set chardet==3.0.4 for Python 3.


## [2.2.5] - 2024-11-11
- Updated chardet==4.0.0 for Python 3
- Updated distro==1.9.0 for Python 3
- Updated protobuf==3.19.6 for Python 3
- Updated mysql-connector-python==8.0.28 for Python 3
- Updated mysql-lib to v5.3.8
- Updated python-lib to v3.0.7
        
### Deprecated
- Support for Python 2.7


## [2.2.4] - 2024-09-27
- Updated simplejson==3.13.2 for Python 3
- Updated python-lib to v3.0.5
- Updated mysql-lib to v5.3.7


## [2.2.3] - 2024-09-10

### Changed
- config/mysql_cfg.py.TEMPLATE:  Changed cfg_file default value.
- main: Removed parsing from gen_class.ArgParser call and called arg_parse2 as part of "if" statement.


## [2.2.2] - 2024-03-07
- Updated to work in Red Hat 8
- Updated python-lib to v3.0.3
- Updated mysql-lib to v5.3.4

### Fixed
- chk_rep_cfg: Replace string version checking with tuple version checking.

### Changed
- chk_rep_cfg: Replaced entries in req_rep_cfg dictionary if version is MySQL v8.0.26 or above.
- Set simplejson to 3.12.0 for Python 3.
- Set chardet to 3.0.4 for Python 2.
- Documentation updates.


## [2.2.1] - 2023-11-02
- Downgraded mysql-lib to v5.3.1
-    Note: The mysql-lib v5.3.1 has not been modified to work in Python 3.

### Fixed
- Changed mysql-lib from v5.3.2 to 5.3.1 due to errors in the mysql-lib package.


## [2.2.0] - 2023-08-21
- Upgraded python-lib to v2.10.1
- Replaced the arg_parser code with gen_class.ArgParser code.

### Changed
- Multiple functions: Replaced the arg_parser code with gen_class.ArgParser code.
- main, dump_load_dbs: Removed gen_libs.get_inst call.


## [2.1.3] - 2022-11-08
- Updated to work in Python 3 too
- Upgraded python-lib to v2.9.4
- Upgraded mysql-lib to v5.3.2

### Changed
- Converted imports to use Python 2.7 or Python 3.


## [2.1.2] - 2022-06-27
- Upgraded python-lib to v2.9.2
- Upgraded mysql-lib to v5.3.1
- Added TLS capability

### Changed
- config/mysql_cfg.py.TEMPLATE: Added TLS entry.
- Documentation updates.


## [2.1.1] - 2022-03-16
- Updated to work with MySQL 8.0.28
- Upgraded python-lib to v2.8.6

### Changed
- dump_load_dbs: Added standard error option to subp.Popen call running the database dump.
- chk_rep_cfg: Set up version check to determine whether to use --master-data or --source-data.
- dump_load_dbs: Changed cmds_gen.is_add_cmd to gen_libs.is_add_cmd.
- crt_dump_cmd: Changed cmds_gen.add_cmd to gen_libs.add_cmd and cmds_gen.is_add_cmd to gen_libs.is_add_cmd.

### Removed
- cmds_gen module

## [2.1.0] - 2020-07-23
- Updated to work in MySQL 8.0 environment.
- Updated to work in MySQL 5.7 environment.
- Updated to use SSL connections.
- Updated to use the mysql_libs v5.2.2 library.

### Fixed
- run_program:  Added disconnect and error message if master and/or slave fails replication requirements check.
- run_program:  Added connect_chk call due to long term dump/restores cause connection timeouts.
- dump_load_dbs:  Fixed problem with mutable default arguments issue.

### Added
- connect_chk:  Checks to see if the connection is still active and reconnect if not.

### Changed
- chk_rep_cfg:  Remove innodb_support_xa from replication config for MySQL 8.0 and above.
- config/mysql_cfg.py.TEMPLATE:  Add SSL configuration entries.
- run_program:  Moved all mysql_libs.disconnect calls to end of function.
- Removed unnecessary \*\*kwargs in function argument list.
- chk_rep:  Replaced manual creation of MasterRep class instance with mysql_libs.create_instance.
- run_program, chk_rep, chk_rep_cfg:  Replaced cmds_gen.disconnect with mysql_libs.disconnect.
- Documentation updates.


## [2.0.3] - 2020-11-13
- Updated to use the mysql_libs v5.0.2 library.
- Updated to work with (much older) mysql.connector v1.1.6 library module.

### Fixed
- run_program:  Master cannot be set to loopback IP if setting up replication.
- config/mysql.cfg.TEMPLATE:  Point to correct socket file.

### Changed
- main:  Set "-r" option to require "-n" option if used.
- run_program:  Added check on opt_arg_list to ensure requirements check was successful.
- run_program, chk_rep_cfg:  Refactored function to remove the sys.exit() command.
- chk_rep:  Replaced mysql_libs.create_instance with manual creation of MasterRep class instance.
- config/mysql_cfg.py.TEMPLATE:  Added replication user information and changed entry name.
- Documentation updates.


## [2.0.2] - 2020-04-20
### Added
- Added ProgramLock class to prevent multiple runs at the same time.
- chk_slv:  Compares the slave's read file and postition with the executed file and position.

### Fixed
- crt_dump_cmd, dump_load_dbs, stop_clr_rep, chk_rep_cfg, chk_slv_err, chk_slv_thr, chk_mst_log, chk_rep, run_program, cfg_chk:  Fixed problem with mutable default arguments issue.
- chk_slv_thr:  Fixed multiple strings.
- dump_load_dbs:  Fixed handling subprocess line.
- main:  Fixed handling command line arguments.
- main:  Added arg_parser.arg_dir_chk_crt call to check directory arguments.
- chk_rep:  Added connect calls for master and slave instances.

### Changed
- chk_mst_log:  Replaced return variables with placeholders for non-used variables.
- stop_clr_rep:  Replace clone.sql() with call to mysql_libs.reset_slave().
- main: Added ProgramLock class to implement program locking.
- config/mysql.cfg.TEMPLATE:  Changed format of template.
- config/mysql_cfg.py.TEMPLATE:  Changed format of template.
- chk_rep:  Removed master argument in chk_slv_err and chk_slv_thr calls - no longer required.
- chk_slv_thr, chk_slv_err: Removed master argument - no longer required.
- chk_mst_log: Removed get_log_info and get_name calls - no longer required.
- main:  Refactor "if" statements to streamline the checking process.
- cfg_chk, chk_slv_thr, chk_mst_log, chk_rep, stop_clr_rep, run_program, chk_rep_cfg, dump_load_dbs, crt_dump_cmd, chk_slv_err:  Changed variables to standard naming convention.
- chk_mst_log:  Added call to chk_slv function.
- Documentation updates.


## [2.0.1] - 2018-11-30
### Changed
- Added \*\*kwargs to a number of function declarations to allow passing of keyword arguments.
- chk_rep_cfg:  Removed passing replication instances to cfg_chk call.
- cfg_chk:  Removed non-used SERVER variable.


## [2.0.0] - 2018-06-04
Breaking Change

### Changed
- stop_clr_rep:  Changed mysql_libs.Show_Slave_Stat and mysql_libs.Stop_Slave to mysql_class references.
- Changed calls to mysql_class, mysql_libs, cmds_gen, gen_libs, and arg_parser to new naming schema.
- Changed function names from uppercase to lowercase.
- Setup single-source version control.


## [1.9.0] - 2018-05-02

### Changed
- Changed "server" to "mysql_class" module reference.
- Changed "commands" to "mysql_libs" module reference.
- Dump_Load_Dbs:  Replaced "mysql_db_dump.Crt_Dump_Cmd" with "Crt_Dump_Cmd" call.
- Chk_Rep:  Replaced "mysql_rep_admin.Chk_Slv_Err" with "Chk_Slv_Err" call.
- Chk_Rep:  Replaced "mysql_rep_admin.Chk_Slv_Thr" with "Chk_Slv_Thr" call.
- Chk_Rep:  Replaced "mysql_rep_admin.Chk_Mst_Log" with "Chk_Mst_Log" call.

### Added
- Chk_Mst_Log
- Chk_Slv_Thr
- Chk_Slv_Err
- Crt_Dump_Cmd
- Added single-source version control.


## [1.8.0] - 2017-08-25
### Changed
- Run_Program:  Check to see if the extra default config file is valid.


## [1.7.0] - 2017-08-18
### Changed
- Help_Message:  Replace docstring with printing the programs \_\_doc\_\_.
- Change single quotes to double quotes.
- Convert program to use local libraries from ./lib directory.


## [1.6.0] - 2016-12-16
### Changed
- Dump_Load_Dbs:  Add --set-gtid-purge option to dump command if the Source and Clone GTID modes do not match, Clone is not GTID enabled, and replication is not being setup.  Equivalent to adding the "-r" argument.
- Run_Program:  Added check to see if replication is being setup.


## [1.5.0] - 2016-11-21
### Changed
- MySQL 5.6 (GTID enabled) error fix for MySQL Error 1776 and mysqldump Error 32 on writes.
- Chk_Rep_Cfg:  If dump is to be part of replication then do not include "change master to" in dump file if the Clone database is GTID enabled.


## [1.4.0] - 2016-10-31
### Changed
- MySQL 5.6 (GTID enabled) requires additional dump options and additional steps to load the database.  Also included an argument to remove GTIDs from dump file, if required.
- main:  Modified/added variabes for MySQL 5.6 (GTID).
- Run_Program:  Check to see if the Source and Clone database GTID modes match.
- Dump_Load_Dbs:  Modified dump command to include additional options and reset database if its GTID enabled.


## [1.3.0] - 2016-10-12
### Changed
- MySQL 5.6 now gives warning if password is passed on the command line.  To suppress this warning, will require the use of the --defaults-extra-file option.  This will require the use of updated commands library and server class files.  See in documentation above for exact version required for MySQL 5.6.


## [1.2.0] - 2016-09-09
### Changed
- Changed the option -c and -C so they are aligned with the other programs.  -c is now for master/source and -t for slave/clone database.
- Run_Program, Chk_Rep:  Changed -C to -c and -c to -t.  Changed commands.Disconnect() to cmds_gen.Disconnect().
- main:  Changed -C to -t.  Replaced Arg_Parse with Arg_Parse2, reorganized the main 'if' statements, and streamlined the check process.
- Chk_Rep_Cfg:  Changed commands.Disconnect() to cmds_gen.Disconnect().
- Dump_Load_Dbs:  Changed my_prog.Crt_Cmd to commands.Crt_Cmd.


## [1.1.0] - 2015-12-21
### Changed
- Chk_Rep_Cfg function.
- Cfg_Chk function.


## [1.0.0] - 2015-12-17
- Initial creation.

