#!/usr/bin/python
# Classification (U)

"""Program:  mysql_clone.py

    Description:  To clone a database to another database server.  The new
        database can either be a standalone copy of the original database or
        the program can integrate the new database into replication with the
        original database creating a master-slave replication setup.

    Usage:
        mysql_clone.py -c mysql_cfg_master -t mysql_cfg_slave -d path
            [-n [-r]] [-p path] [-y flavor_id]
            [-v | -h]

    Arguments:
        -c filename => Source/Master configuration file.  Required arg.
        -t filename => Clone/Slave configuration file.  Required arg.
        -d dir_path => Directory path to config files.  Required arg.
        -n => No replication, create a clone of the master database.
        -r => Remove GTID entries from dump file.  Requires the -n option.
        -p dir_path => Directory path to mysql programs.  Only required if the
            mysql binary programs do not run properly.  (i.e. not in the $PATH
            variable.)
        -y value => A flavor id for the program lock.  To create unique lock.
        -v => Display version of this program.
        -h => Help and usage message.
            NOTE:  -v or -h overrides the other options.

    Notes:
        Master and Slave config file format (config/mysql_cfg.py.TEMPLATE):
            # Configuration file for database server:
            user = 'USER'
            japd = 'PSWORD'
            rep_user = 'REP_USER'
            rep_japd = 'REP_PSWORD'
            # DO NOT USE 127.0.0.1 or localhost for the master, use actual IP.
            host = 'IP_ADDRESS'
            name = 'HOSTNAME'
            sid = SERVER_ID
            extra_def_file = 'PYTHON_PROJECT/config/mysql.cfg'
            serv_os = 'Linux'
            port = 3306
            cfg_file = 'MYSQL_DIRECTORY/mysqld.cnf'

            # If SSL connections are being used, configure one or more of these
                entries:
            ssl_client_ca = None
            ssl_client_key = None
            ssl_client_cert = None

            # Only changes these if necessary and have knowledge in MySQL
                SSL configuration setup:
            ssl_client_flag = None
            ssl_disabled = False
            ssl_verify_id = False
            ssl_verify_cert = False

            # Set what TLS versions are allowed in the connection set up:
            tls_versions = []

        NOTE 1:  Include the cfg_file even if running remotely as the
            file will be used in future releases.
        NOTE 2:  In MySQL 5.6 - it now gives warning if password is passed on
            the command line.  To suppress this warning, will require the use
            of the --defaults-extra-file option (i.e. extra_def_file) in the
            database configuration file.  See below for the
            defaults-extra-file format.

        configuration modules -> name is runtime dependent as it can be
            used to connect to different databases with different names.

        Defaults Extra File format (config/mysql.cfg.TEMPLATE):
            [client]
            password='PSWORD'
            socket=DIRECTORY_PATH/mysql.sock

        NOTE 1:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.
        NOTE 2:  If running on a MySQL 5.7 database, turn on the
            "show_compatibility_56" option to simulate a MySQL 5.6 server for
            the Global Variable status.
        NOTE 3:  The --defaults-extra-file option will be overridden if there
            is a ~/.my.cnf or ~/.mylogin.cnf file located in the home directory
            of the user running this program.  The extras file will in effect
            be ignored.
        NOTE 4:  Socket use is only required to be set in certain conditions
            when connecting using the local host.

    Example:
        mysql_clone.py -c master_cfg -t slave_cfg -d config

"""

# Libraries and Global Variables

# Standard
import sys
import subprocess
import time

# Local
try:
    from .lib import gen_libs
    from .lib import gen_class
    from .mysql_lib import mysql_libs
    from .mysql_lib import mysql_class
    from . import version

except (ValueError, ImportError) as err:
    import lib.gen_libs as gen_libs                     # pylint:disable=R0402
    import lib.gen_class as gen_class                   # pylint:disable=R0402
    import mysql_lib.mysql_libs as mysql_libs           # pylint:disable=R0402
    import mysql_lib.mysql_class as mysql_class         # pylint:disable=R0402
    import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def cfg_chk(func_call, cfg_dict):

    """Function:  cfg_chk

    Description:  Checks the configuration of a database for replication.

    Arguments:
        (input) func_call -> Method call to return config settings
        (input) cfg_dict -> Dictionary of configuration items to check
        (output) cfg_flag -> True or False - Configuration passes

    """

    cfg_dict = dict(cfg_dict)
    cfg_flag = True
    cls_cfg_dict = func_call()

    for item in cfg_dict:
        if item in cls_cfg_dict:

            # Does server config not match class config
            if cfg_dict[item] != cls_cfg_dict[item]:

                # Read_only will produce a warning, everything else an error
                if item == "read_only":
                    print(f"Warning: {item} not set for slave.")

                else:
                    cfg_flag = False
                    print(f"Error:  {item} not set correctly.")

        else:
            cfg_flag = False
            print("Error:  Missing option in class.")

    return cfg_flag


def crt_dump_cmd(server, args, opt_arg_list, opt_dump_list):

    """Function:  crt_dump_cmd

    Description:  Create the database dump command line.

    Arguments:
        (input) server -> Database server instance
        (input) args -> ArgParser class instance
        (input) opt_arg_list -> List of commands to add to cmd line
        (input) opt_dump_list -> Dictionary of additional options
        (output) -> Database dump command line

    """

    opt_arg_list = list(opt_arg_list)
    opt_dump_list = dict(opt_dump_list)
    dump_args = mysql_libs.crt_cmd(
        server, args.arg_set_path("-p", cmd="mysqldump"))

    # Add arguments to dump command
    for arg in opt_arg_list:
        dump_args = gen_libs.add_cmd(dump_args, arg=arg)

    # Append additional options to command
    return gen_libs.is_add_cmd(args, dump_args, opt_dump_list)


def dump_load_dbs(source, clone, args, req_rep_cfg, opt_arg_list, **kwargs):

    """Function:  dump_load_dbs

    Description:  Dumps and loads all databases in a single transaction.

    Arguments:
        (input) source -> Source server instance
        (input) clone -> Destination server instance
        (input) args -> ArgParser class instance
        (input) req_rep_cfg -> Required replication config settings
        (input) opt_arg_list -> List of options to add to dump cmd line
        (input) **kwargs:
            opt_dump_list -> Dictionary of additional options

    """

    req_rep_cfg = dict(req_rep_cfg)
    opt_arg_list = list(opt_arg_list)
    dump_cmd = crt_dump_cmd(
        source, args, opt_arg_list, list(kwargs.get("opt_dump_list", [])))
    efile = gen_libs.crt_file_time("mysql_clone_err_log", "/" + "tmp")
    err_file = open(efile, mode="w", encoding="UTF-8")  # pylint:disable=R1732

    if source.gtid_mode != clone.gtid_mode and not clone.gtid_mode \
       and args.arg_exist("-n") and not args.arg_exist("-r"):

        dump_cmd = gen_libs.is_add_cmd(
            {"-r": "True"}, dump_cmd, list(kwargs.get("opt_dump_list", [])))

    load_cmd = mysql_libs.crt_cmd(
        clone, args.arg_set_path("-p", cmd="mysql"))

    if clone.gtid_mode:
        mysql_libs.reset_master(clone)

    # Dump databases, pipe into load, and wait until completed
    proc1 = subprocess.Popen(                           # pylint:disable=R1732
        dump_cmd, stdout=subprocess.PIPE, stderr=err_file)
    proc2 = subprocess.Popen(                           # pylint:disable=R1732
        load_cmd, stdin=proc1.stdout)
    proc2.wait()

    err_file.close()

    if not gen_libs.is_empty_file(efile):
        print(f"Review the contents of error file: {efile}")


def stop_clr_rep(clone, args):

    """Function:  stop_clr_rep

    Description:  Suspends the slave on the Clone and clears the replication
        configuration if this is for a clone only system.

    Arguments:
        (input) clone -> Server instance
        (input) args -> ArgParser class instance

    """

    if mysql_class.show_slave_stat(clone):
        mysql_class.slave_stop(clone)

        if not args.arg_exist("-n"):
            mysql_libs.reset_slave(clone)


def chk_rep_cfg(source, clone, args, req_rep_cfg, opt_arg_list):

    """Function:  chk_rep_cfg

    Description:  Replication configuration check on the source & clone
        servers.

    Arguments:
        (input) source -> Source server instance
        (input) clone -> Destination server instance
        (input) args -> ArgParser class instance
        (input) req_rep_cfg -> Required replication config settings
        (input) opt_arg_list -> List of options to add to dump cmd line
        (output) opt_arg_list -> List of options to add to dump cmd line

    """

    req_rep_cfg = dict(req_rep_cfg)
    opt_arg_list = list(opt_arg_list)

    master_d = "--source-data=" if source.version >= (8, 0, 26) \
        else "--master-data="

    # Replacement of entries for MySQL v8.0.26 and above
    if source.version >= (8, 0, 26):
        req_rep_cfg["slave"].pop("log_slave_updates", None)
        req_rep_cfg["slave"].pop("sync_master_info", None)
        req_rep_cfg["slave"]["log_replica_updates"] = "ON"
        req_rep_cfg["slave"]["sync_source_info"] = "1"

    if not args.arg_exist("-n"):
        source.upd_mst_rep_stat()
        clone.upd_slv_rep_stat()

        # Both servers must meet replication requirements
        if not cfg_chk(source.fetch_mst_rep_cfg, req_rep_cfg["master"]) \
           or not cfg_chk(clone.fetch_slv_rep_cfg, req_rep_cfg["slave"]):

            # Create list to act as a failure of the requirements
            opt_arg_list = []
            mysql_libs.disconnect(source, clone)
            print("Error: Master and/or Slave rep config did not pass.")

        else:
            if clone.gtid_mode:
                # Exclude "change master to" option from dump file
                opt_arg_list.append(master_d + "2")

            else:
                # Include "change master to" option in dump file
                opt_arg_list.append(master_d + "1")

    else:
        # Exclude "change master to" option from dump file
        opt_arg_list.append(master_d + "2")

    return opt_arg_list


def chk_slv_err(slave):

    """Function:  chk_slv_err

    Description:  Check the Slave's IO and SQL threads for errors.

    Arguments:
        (input) slave -> Slave class instance(s)

    """

    slave = list(slave)

    if slave:

        for slv in slave:

            ioerr, sql, io_msg, sql_msg, io_time, sql_time = slv.get_err_stat()
            name = slv.get_name()

            # Is there a IO error
            if ioerr:
                print(f"\nSlave:\t{name}")
                print(f"IO Error Detected:\t{ioerr}")
                print(f"\tIO Message:\t{io_msg}")
                print(f"\tIO Timestamp:\t{io_time}")

            # Is there a SQL error
            if sql:
                print(f"\nSlave:\t{name}")
                print(f"SQL Error Detected:\t{sql}")
                print(f"\tSQL Message:\t{sql_msg}")
                print(f"\tSQL Timestamp:\t{sql_time}")

    else:
        print("\nchk_slv_err:  Warning:  No Slave instance detected.")


def chk_slv_thr(slave):

    """Function:  chk_slv_thr

    Description:  Checks the status of the Slave(s) IO and SQL threads.

    Arguments:
        (input) slave -> Slave class instance(s)

    """

    slave = list(slave)

    if slave:

        for slv in slave:
            thr, io_thr, sql_thr, run = slv.get_thr_stat()
            name = slv.get_name()

            # Check slave IO state and slave running attributes
            if not thr or not gen_libs.is_true(run):
                print(f"\nSlave:  {name}")
                print("Error:  Slave IO/SQL Threads are down.")

            # Check slave IO running attribute
            elif not gen_libs.is_true(io_thr):
                print(f"\nSlave:  {name}")
                print("Error:  Slave IO Thread is down.")

            # Check slave SQL running attribute
            elif not gen_libs.is_true(sql_thr):
                print(f"\nSlave:  {name}")
                print("Error:  Slave SQL Thread is down.")

    else:
        print("\nchk_slv_thr:  Warning:  No Slave instance detected.")


def chk_slv(slave):

    """Function:  chk_slv

    Description:  Compares the Slave's read file and postition with the
        executed file and position.  Will also print GTID info, in pre-MySQL
        5.6 this will be NULL.

    Arguments:
        (input) slave -> Slave instance

    """

    mst_file, relay_file, read_pos, exec_pos = slave.get_log_info()
    name = slave.get_name()

    # Slave's master info doesn't match slave's relay info
    if mst_file != relay_file or read_pos != exec_pos:
        print(f"\nSlave: {name}")
        print("Warning:  Slave might be lagging in execution of log.")
        print(f"\tRead Log:\t{mst_file}")
        print(f"\tRead Pos:\t{read_pos}")

        if slave.gtid_mode:
            print(f"\tRetrieved GTID:\t{slave.retrieved_gtid}")

        print(f"\tExec Log:\t{relay_file}")
        print(f"\tExec Pos:\t{exec_pos}")

        if slave.gtid_mode:
            print(f"\tExecuted GTID:\t{slave.exe_gtid}")


def chk_mst_log(master, slave, **kwargs):

    """Function:  chk_mst_log

    Description:  Compares the binary log and position between the master and
        slave(s) and also compares the read and execute positions of
        the log on the slave itself.

    Arguments:
        (input) master -> Master class instance
        (input) slave -> Slave class instance(s)

    """

    slave = list(slave)

    if master and slave:
        fname, log_pos = master.get_log_info()

        for slv in slave:
            mst_file, _, read_pos, _ = slv.get_log_info()
            name = slv.get_name()

            # If master's log file or position doesn't match slave's log info
            if fname != mst_file or log_pos != read_pos:

                print("\nWarning:  Slave lagging in reading master log.")
                print(f"Master: {master.name}")
                print(f"\tMaster Log: {fname}")
                print(f"\t\tMaster Pos: {log_pos}")
                print(f"Slave: {name}")
                print(f"\tSlave Log: {mst_file}")
                print(f"\t\tSlave Pos: {read_pos}")

            chk_slv(slv, **kwargs)

    elif slave:
        print("\nchk_mst_log:  Warning:  Missing Master instance.")

        for slv in slave:
            chk_slv(slv, **kwargs)

    else:
        print("\nchk_mst_log:  Warning:  Missing Master and Slave instances.")


def chk_rep(clone, args):

    """Function:  chk_rep

    Description:  Create master and slave instances and check the status of the
        replication system between the two servers.

    Arguments:
        (input) clone -> Destination server instance
        (input) args -> ArgParser class instance

    """

    if not args.arg_exist("-n"):
        master = mysql_libs.create_instance(
            args.get_val("-c"), args.get_val("-d"), mysql_class.MasterRep)
        master.connect()
        mysql_libs.change_master_to(master, clone)
        slave = mysql_libs.create_instance(
            args.get_val("-t"), args.get_val("-d"), mysql_class.SlaveRep)
        slave.connect()
        slave.start_slave()

        # Wait for slave to start
        time.sleep(5)
        master.upd_mst_status()
        slave.upd_slv_status()
        chk_slv_err([slave])
        chk_slv_thr([slave])
        chk_mst_log(master, [slave])
        mysql_libs.disconnect(master, slave)


def connect_chk(server):

    """Function:  connect_chk

    Description:  Checks to see if the connection is still active and if not
        then reconnects the database instance.

    Arguments:
        (input) server -> Database instance

    """

    if not server.is_connected():
        server.connect()


def run_program(args, req_rep_cfg, opt_arg_list, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.
        Also determines whether the cloning operation is for replication or as
        a stand-along server.

    Arguments:
        (input) args -> ArgParser class instance
        (input) req_rep_cfg -> Required replication config settings
        (input) opt_arg_list -> List of options to add to dump cmd line
        (input) **kwargs:
            opt_dump_list -> Dictionary of additional options

    """

    req_rep_cfg = dict(req_rep_cfg)
    opt_arg_list = list(opt_arg_list)
    source = mysql_libs.create_instance(
        args.get_val("-c"), args.get_val("-d"), mysql_class.Server)
    clone = mysql_libs.create_instance(
        args.get_val("-t"), args.get_val("-d"), mysql_class.Server)
    source.connect()
    source.set_srv_gtid()
    clone.connect()
    clone.set_srv_gtid()

    status, status_msg = mysql_libs.is_cfg_valid([source, clone])

    # Master cannot be set to loopback IP if setting up replication
    if source.host in ["127.0.0.1", "localhost"] \
       and not args.arg_exist("-n"):

        status = False
        status_msg.append("Master host entry has incorrect entry.")
        status_msg.append(f"Master host: {source.host}")

    if status:

        # Do not proceed if GTID modes don't match
        if source.gtid_mode != clone.gtid_mode and not args.arg_exist("-n"):
            print(f"Error:  Source {source.gtid_mode} and Clone"
                  f" {clone.gtid_mode} GTID modes do not match.")

        else:
            stop_clr_rep(clone, args)

            # Add to argument list array based on rep config
            opt_arg_list = chk_rep_cfg(
                source, clone, args, req_rep_cfg, opt_arg_list)

            # If empty list, then failure in requirements check
            if opt_arg_list:
                print("Starting dump-load process...")
                dump_load_dbs(
                    source, clone, args, req_rep_cfg, opt_arg_list, **kwargs)
                print("Finished dump-load process...")

                # Long term processes cause connection timeouts
                connect_chk(clone)
                chk_rep(clone, args)

            else:
                print("Error:  Master/Slave do not meet rep requirements.")

    else:
        print("Error:  Detected problem in the configuration file.")

        for msg in status_msg:
            print(msg)

    mysql_libs.disconnect(source, clone)


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_perms_chk -> contains directories and their octal permissions
        opt_arg_list -> contains arguments to add to command line by default
        opt_con_req_list -> contains the options that require other options
        opt_dump_list -> contains optional arguments for mysqldump command
        opt_req_list -> contains the options that are required for the program
        opt_val_list -> contains options which require values
        req_rep_cfg -> contains replication config settings got master/slave

    Arguments:
        (input) argv -> Arguments from the command line

    """

    dir_perms_chk = {"-d": 5, "-p": 5}
    opt_arg_list = [
        "--single-transaction", "--all-databases", "--triggers", "--routines",
        "--events", "--ignore-table=mysql.event"]
    opt_con_req_list = {"-r": ["-n"]}
    opt_dump_list = {"-r": "--set-gtid-purged=OFF"}
    opt_req_list = ["-c", "-t", "-d"]
    opt_val_list = ["-c", "-t", "-d", "-p", "-y"]
    req_rep_cfg = {
        "master": {
            "log_bin": "ON", "sync_binlog": "1",
            "innodb_flush_log_at_trx_commit": "1", "binlog_format": "ROW"},
        "slave": {
            "log_bin": "ON", "read_only": "ON", "log_slave_updates": "ON",
            "sync_master_info": "1", "sync_relay_log": "1",
            "sync_relay_log_info": "1"}}

    # Process argument list from command line
    args = gen_class.ArgParser(sys.argv, opt_val=opt_val_list)

    if args.arg_parse2()                                            \
       and not gen_libs.help_func(args, __version__, help_message)  \
       and args.arg_cond_req(opt_con_req=opt_con_req_list)          \
       and args.arg_require(opt_req=opt_req_list)                   \
       and args.arg_dir_chk(dir_perms_chk=dir_perms_chk):

        try:
            proglock = gen_class.ProgramLock(
                sys.argv, args.get_val("-y", def_val=""))
            run_program(
                args, req_rep_cfg, opt_arg_list, opt_dump_list=opt_dump_list)
            del proglock

        except gen_class.SingleInstanceException:
            print(f'WARNING:  lock in place for mysql_clone with id of:'
                  f' {args.get_val("-y", def_val="")}')


if __name__ == "__main__":
    sys.exit(main())
