#!/usr/bin/python
# Classification (U)

"""Program:  mysql_clone.py

    Description:  To clone a database to another database server.  The new
        database can either be a standalone copy of the original database or
        the program can integrate the new database into replication with the
        original database creating a master-slave replication setup.

    Usage:
        mysql_clone.py -c master_file -t slave_file -d path
            [-n [-r]] [-p path] [-y flavor_id]
            [-v | -h]

    Arguments:
        -c file => Source/Master configuration file.  Required arg.
        -t file => Clone/Slave configuration file.  Required arg.
        -d dir path => Directory path to config files.  Required arg.
        -n => No replication, create a clone of the master database.
        -r => Remove GTID entries from dump file.  Requires the -n option.
        -p dir path => Directory path to mysql programs.  Only required if the
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
            password='PASSWORD'
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

    Example:
        mysql_clone.py -c master_cfg -t slave_cfg -d config

"""

# Libraries and Global Variables

# Standard
import sys
import subprocess
import time

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.cmds_gen as cmds_gen
import lib.gen_class as gen_class
import lib.machine as machine
import mysql_lib.mysql_libs as mysql_libs
import mysql_lib.mysql_class as mysql_class
import version

__version__ = version.__version__


def help_message():

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def cfg_chk(func_call, cfg_dict, **kwargs):

    """Function:  cfg_chk

    Description:  Checks the configuration of a database for replication.

    Arguments:
        (input) func_call -> Method call to return config settings.
        (input) cfg_dict -> Dictionary of configuration items to check.
        (output) cfg_flag -> True or False - Configuration passes.

    """

    cfg_dict = dict(cfg_dict)
    cfg_flag = True
    cls_cfg_dict = func_call()

    for item in cfg_dict:
        if item in cls_cfg_dict:

            # Does server config not match class config.
            if cfg_dict[item] != cls_cfg_dict[item]:

                # Read_only will produce a warning, everything else an error.
                if item == "read_only":
                    print("Warning: {0} not set for slave.".format(item))

                else:
                    cfg_flag = False
                    print("Error:  {0} not set correctly.".format(item))

        else:
            cfg_flag = False
            print("Error:  Missing option in class.")

    return cfg_flag


def crt_dump_cmd(server, args_array, opt_arg_list, opt_dump_list, **kwargs):

    """Function:  crt_dump_cmd

    Description:  Create the database dump command line.

    Arguments:
        (input) server -> Database server instance.
        (input) args_array -> Array of command line options and values.
        (input) opt_arg_list -> List of commands to add to cmd line.
        (input) opt_dump_list -> Dictionary of additional options.
        (output) -> Database dump command line.

    """

    args_array = dict(args_array)
    opt_arg_list = list(opt_arg_list)
    opt_dump_list = dict(opt_dump_list)
    dump_args = mysql_libs.crt_cmd(
        server, arg_parser.arg_set_path(args_array, "-p") + "mysqldump")

    # Add arguments to dump command.
    for arg in opt_arg_list:
        dump_args = cmds_gen.add_cmd(dump_args, arg=arg)

    # Append additional options to command.
    return cmds_gen.is_add_cmd(args_array, dump_args, opt_dump_list)


def dump_load_dbs(source, clone, args_array, req_rep_cfg, opt_arg_list,
                  **kwargs):

    """Function:  dump_load_dbs

    Description:  Dumps and loads all databases in a single transaction.

    Arguments:
        (input) source -> Source server instance.
        (input) clone -> Destination server instance.
        (input) args_array -> Array of command line options and values.
        (input) req_rep_cfg -> Required replication config settings.
        (input) opt_arg_list -> List of options to add to dump cmd line.
        (input) **kwargs:
            opt_dump_list -> Dictionary of additional options.

    """

    args_array = dict(args_array)
    req_rep_cfg = dict(req_rep_cfg)
    opt_arg_list = list(opt_arg_list)
    subp = gen_libs.get_inst(subprocess)
    dump_cmd = crt_dump_cmd(source, args_array, opt_arg_list,
                            kwargs.get("opt_dump_list", []))

    if source.gtid_mode != clone.gtid_mode and not clone.gtid_mode \
       and "-n" in args_array and "-r" not in args_array:

        dump_cmd = cmds_gen.is_add_cmd({"-r": "True"}, dump_cmd,
                                       kwargs.get("opt_dump_list", []))

    load_cmd = mysql_libs.crt_cmd(
        clone, arg_parser.arg_set_path(args_array, "-p") + "mysql")

    if clone.gtid_mode:
        mysql_libs.reset_master(clone)

    # Dump databases, pipe into load, and wait until completed.
    proc1 = subp.Popen(dump_cmd, stdout=subp.PIPE)
    proc2 = subp.Popen(load_cmd, stdin=proc1.stdout)
    proc2.wait()


def stop_clr_rep(clone, args_array, **kwargs):

    """Function:  stop_clr_rep

    Description:  Suspends the slave on the Clone and clears the replication
        configuration if this is for a clone only system.

    Arguments:
        (input) clone -> Server instance.
        (input) args_array -> Array of command line options and values.

    """

    args_array = dict(args_array)

    if mysql_class.show_slave_stat(clone):
        mysql_class.slave_stop(clone)

        if "-n" in args_array:
            mysql_libs.reset_slave(clone)


def chk_rep_cfg(source, clone, args_array, req_rep_cfg, opt_arg_list,
                **kwargs):

    """Function:  chk_rep_cfg

    Description:  Replication configuration check on the source & clone
        servers.

    Arguments:
        (input) source -> Source server instance.
        (input) clone -> Destination server instance.
        (input) args_array -> Array of command line options and values.
        (input) req_rep_cfg -> Required replication config settings.
        (input) opt_arg_list -> List of options to add to dump cmd line.
        (output) opt_arg_list -> List of options to add to dump cmd line.

    """

    args_array = dict(args_array)
    req_rep_cfg = dict(req_rep_cfg)
    opt_arg_list = list(opt_arg_list)

    if "-n" not in args_array:
        source.upd_mst_rep_stat()
        clone.upd_slv_rep_stat()

        # Both servers must meet replication requirements.
        if not cfg_chk(source.fetch_mst_rep_cfg, req_rep_cfg["master"]) \
           or not cfg_chk(clone.fetch_slv_rep_cfg, req_rep_cfg["slave"]):

            # Create list to act as a failure of the requirements.
            opt_arg_list = list()
            cmds_gen.disconnect(source, clone)
            print("Error: Master and/or Slave rep config did not pass.")

        else:
            if clone.gtid_mode:
                # Exclude "change master to" option from dump file.
                opt_arg_list.append("--master-data=2")

            else:
                # Include "change master to" option in dump file.
                opt_arg_list.append("--master-data=1")

    else:
        # Exclude "change master to" option from dump file.
        opt_arg_list.append("--master-data=2")

    return opt_arg_list


def chk_slv_err(slave, **kwargs):

    """Function:  chk_slv_err

    Description:  Check the Slave's IO and SQL threads for errors.

    Arguments:
        (input) slave -> Slave class instance(s).

    """

    slave = list(slave)

    if slave:

        for slv in slave:

            ioerr, sql, io_msg, sql_msg, io_time, sql_time = slv.get_err_stat()
            name = slv.get_name()

            # Is there a IO error
            if ioerr:
                print("\nSlave:\t{0}".format(name))
                print("IO Error Detected:\t{0}".format(ioerr))
                print("\tIO Message:\t{0}".format(io_msg))
                print("\tIO Timestamp:\t{0}".format(io_time))

            # Is there a SQL error
            if sql:
                print("\nSlave:\t{0}".format(name))
                print("SQL Error Detected:\t{0}".format(sql))
                print("\tSQL Message:\t{0}".format(sql_msg))
                print("\tSQL Timestamp:\t{0}".format(sql_time))

    else:
        print("\nchk_slv_err:  Warning:  No Slave instance detected.")


def chk_slv_thr(slave, **kwargs):

    """Function:  chk_slv_thr

    Description:  Checks the status of the Slave(s) IO and SQL threads.

    Arguments:
        (input) slave -> Slave class instance(s).

    """

    slave = list(slave)
    prt_template = "\nSlave:  {0}"

    if slave:

        for slv in slave:
            thr, io_thr, sql_thr, run = slv.get_thr_stat()
            name = slv.get_name()

            # Check slave IO state and slave running attributes.
            if not thr or not gen_libs.is_true(run):
                print(prt_template.format(name))
                print("Error:  Slave IO/SQL Threads are down.")

            # Check slave IO running attribute.
            elif not gen_libs.is_true(io_thr):
                print(prt_template.format(name))
                print("Error:  Slave IO Thread is down.")

            # Check slave SQL running attribute.
            elif not gen_libs.is_true(sql_thr):
                print(prt_template.format(name))
                print("Error:  Slave SQL Thread is down.")

    else:
        print("\nchk_slv_thr:  Warning:  No Slave instance detected.")


def chk_slv(slave, **kwargs):

    """Function:  chk_slv

    Description:  Compares the Slave's read file and postition with the
        executed file and position.  Will also print GTID info, in pre-MySQL
        5.6 this will be NULL.

    Arguments:
        (input) slave -> Slave instance.

    """

    mst_file, relay_file, read_pos, exec_pos = slave.get_log_info()
    name = slave.get_name()

    # Slave's master info doesn't match slave's relay info.
    if mst_file != relay_file or read_pos != exec_pos:
        print("\nSlave: {0}".format(name))
        print("Warning:  Slave might be lagging in execution of log.")
        print("\tRead Log:\t{0}".format(mst_file))
        print("\tRead Pos:\t{0}".format(read_pos))

        if slave.gtid_mode:
            print("\tRetrieved GTID:\t{0}".format(slave.retrieved_gtid))

        print("\tExec Log:\t{0}".format(relay_file))
        print("\tExec Pos:\t{0}".format(exec_pos))

        if slave.gtid_mode:
            print("\tExecuted GTID:\t{0}".format(slave.exe_gtid))


def chk_mst_log(master, slave, **kwargs):

    """Function:  chk_mst_log

    Description:  Compares the binary log and position between the master and
        slave(s) and also compares the read and execute positions of
        the log on the slave itself.

    Arguments:
        (input) master -> Master class instance.
        (input) slave -> Slave class instance(s).

    """

    slave = list(slave)

    if master and slave:
        fname, log_pos = master.get_log_info()

        for slv in slave:
            mst_file, _, read_pos, _ = slv.get_log_info()
            name = slv.get_name()

            # If master's log file or position doesn't match slave's log info.
            if fname != mst_file or log_pos != read_pos:

                print("\nWarning:  Slave lagging in reading master log.")
                print("Master: {0}".format(master.name))
                print("\tMaster Log: {0}".format(fname))
                print("\t\tMaster Pos: {0}".format(log_pos))
                print("Slave: {0}".format(name))
                print("\tSlave Log: {0}".format(mst_file))
                print("\t\tSlave Pos: {0}".format(read_pos))

            chk_slv(slv, **kwargs)

    elif slave:
        print("\nchk_mst_log:  Warning:  Missing Master instance.")

        for slv in slave:
            chk_slv(slv, **kwargs)

    else:
        print("\nchk_mst_log:  Warning:  Missing Master and Slave instances.")


def chk_rep(clone, args_array, **kwargs):

    """Function:  chk_rep

    Description:  Create master and slave instances and check the status of the
        replication system between the two servers.

    Arguments:
        (input) clone -> Destination server instance.
        (input) args_array -> Array of command line options and values.

    """

    args_array = dict(args_array)

    if "-n" not in args_array:
        cfg = gen_libs.load_module(args_array["-c"], args_array["-d"])
        master = mysql_class.MasterRep(
            cfg.name, cfg.sid, cfg.user, cfg.japd,
            os_type=getattr(machine, cfg.serv_os)(), host=cfg.host,
            port=cfg.port,
            defaults_file=cfg.cfg_file,
            extra_def_file=cfg.__dict__.get("extra_def_file", None),
            rep_user=cfg.rep_user, rep_japd=cfg.rep_japd)
        master.connect()
        mysql_libs.change_master_to(master, clone)
        slave = mysql_libs.create_instance(args_array["-t"], args_array["-d"],
                                           mysql_class.SlaveRep)
        slave.connect()
        slave.start_slave()

        # Waiting for slave to start.
        time.sleep(5)
        master.upd_mst_status()
        slave.upd_slv_status()
        chk_slv_err([slave])
        chk_slv_thr([slave])
        chk_mst_log(master, [slave])
        cmds_gen.disconnect(master, slave)


def run_program(args_array, req_rep_cfg, opt_arg_list, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.
        Also determines whether the cloning operation is for replication or as
        a stand-along server.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) req_rep_cfg -> Required replication config settings.
        (input) opt_arg_list -> List of options to add to dump cmd line.
        (input) **kwargs:
            opt_dump_list -> Dictionary of additional options.

    """

    args_array = dict(args_array)
    req_rep_cfg = dict(req_rep_cfg)
    opt_arg_list = list(opt_arg_list)
    source = mysql_libs.create_instance(args_array["-c"], args_array["-d"],
                                        mysql_class.Server)
    clone = mysql_libs.create_instance(args_array["-t"], args_array["-d"],
                                       mysql_class.Server)
    source.connect()
    source.set_srv_gtid()
    clone.connect()
    clone.set_srv_gtid()
    status, status_msg = mysql_libs.is_cfg_valid([source, clone])

    # Master cannot be set to loopback IP if setting up replication.
    if source.host in ["127.0." + "0.1", "localhost"] \
       and "-n" not in args_array:

        status = False
        status_msg.append("Master host entry has incorrect entry.")
        status_msg.append("Master host: %s" % (source.host))

    if status:

        # Do not proceed if GTID modes don't match and rep is being configured.
        if source.gtid_mode != clone.gtid_mode and "-n" not in args_array:
            cmds_gen.disconnect(source, clone)
            print("Error:  Source (%s) and Clone (%s) GTID modes do not match."
                  % (source.gtid_mode, clone.gtid_mode))

        else:
            stop_clr_rep(clone, args_array)

            # Add to argument list array based on rep config.
            opt_arg_list = chk_rep_cfg(source, clone, args_array, req_rep_cfg,
                                       opt_arg_list)

            # If empty list, then failure in requirements check.
            if opt_arg_list:
                print("Starting dump-load process...")
                dump_load_dbs(source, clone, args_array, req_rep_cfg,
                              opt_arg_list, **kwargs)
                print("Finished dump-load process...")
                chk_rep(clone, args_array)
                cmds_gen.disconnect(source, clone)

    else:
        cmds_gen.disconnect(source, clone)
        print("Error:  Detected problem in the configuration file.")

        for msg in status_msg:
            print(msg)


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        opt_arg_list -> contains arguments to add to command line by default.
        opt_con_req_list -> contains the options that require other options.
        opt_dump_list -> contains optional arguments for mysqldump command.
        opt_req_list -> contains the options that are required for the program.
        opt_val_list -> contains options which require values.
        req_rep_cfg -> contains replication config settings got master/slave.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    cmdline = gen_libs.get_inst(sys)
    dir_chk_list = ["-d", "-p"]
    opt_arg_list = ["--single-transaction", "--all-databases", "--triggers",
                    "--routines", "--events", "--ignore-table=mysql.event"]
    opt_con_req_list = {"-r": ["-n"]}
    opt_dump_list = {"-r": "--set-gtid-purged=OFF"}
    opt_req_list = ["-c", "-t", "-d"]
    opt_val_list = ["-c", "-t", "-d", "-p", "-y"]
    req_rep_cfg = {"master": {"log_bin": "ON", "sync_binlog": "1",
                              "innodb_flush_log_at_trx_commit": "1",
                              "innodb_support_xa": "ON",
                              "binlog_format": "ROW"},
                   "slave": {"log_bin": "ON", "read_only": "ON",
                             "log_slave_updates": "ON",
                             "sync_master_info": "1", "sync_relay_log": "1",
                             "sync_relay_log_info": "1"}}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(cmdline.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message) \
       and arg_parser.arg_cond_req(args_array, opt_con_req_list) \
       and not arg_parser.arg_require(args_array, opt_req_list) \
       and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):

        try:
            proglock = gen_class.ProgramLock(cmdline.argv,
                                             args_array.get("-y", ""))
            run_program(args_array, req_rep_cfg, opt_arg_list,
                        opt_dump_list=opt_dump_list)
            del proglock

        except gen_class.SingleInstanceException:
            print("WARNING:  lock in place for mysql_clone with id of: %s"
                  % (args_array.get("-y", "")))


if __name__ == "__main__":
    sys.exit(main())
