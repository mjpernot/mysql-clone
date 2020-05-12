#!/usr/bin/python
# Classification (U)

"""Program:  mysql_clone.py

    Description:  The program can clone a database.  The new database can
        either be a standalone copy of the original database or the program
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
        Master and Slave config file format (config/mysql_cfg.py.TEMPLATE):
            # Configuration file for database server:
            user = "root"
            passwd = "ROOT_PASSWORD"
            # DO NOT USE 127.0.0.1 for the master, use actual IP.
            host = "IP_ADDRESS"
            serv_os = "Linux" or "Solaris"
            name = "HOSTNAME"
            # Default port for Mysql is 3306.
            port = PORT_NUMBER
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

        Defaults Extra File format (config/mysql.cfg.TEMPLATE):
            [client]
            password="ROOT_PASSWORD"
            socket="DIRECTORY_PATH/mysql.sock"

        NOTE:  The socket information can be obtained from the my.cnf
            file under ~/mysql directory.

    Example:
        mysql_clone.py -c source -t target -d config -n

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

    cfg_flag = True
    cls_cfg_dict = func_call()

    for x in cfg_dict:

        if x in cls_cfg_dict:

            # Does server config not match class config.
            if cfg_dict[x] != cls_cfg_dict[x]:

                # Read_only will produce a warning, everything else an error.
                if x == "read_only":
                    print("Warning: {0} variable not set for slave.".format(x))

                else:
                    cfg_flag = False
                    print("Error:  {0} variable not set correctly.".format(x))

        else:
            cfg_flag = False
            print("Error:  Missing option in class.")

    return cfg_flag


def crt_dump_cmd(SERVER, args_array, opt_arg_list, opt_dump_list, **kwargs):

    """Function:  crt_dump_cmd

    Description:  Create the database dump command line.

    Arguments:
        (input) SERVER -> Database server instance.
        (input) args_array -> Array of command line options and values.
        (input) opt_arg_list -> List of commands to add to cmd line.
        (input) opt_dump_list -> Dictionary of additional options.
        (output) -> Database dump command line.

    """

    dump_args = mysql_libs.crt_cmd(SERVER,
                                   arg_parser.arg_set_path(args_array, "-p") +
                                   "mysqldump")

    # Add arguments to dump command.
    for arg in opt_arg_list:
        dump_args = cmds_gen.add_cmd(dump_args, arg=arg)

    # Append additional options to command.
    return cmds_gen.is_add_cmd(args_array, dump_args, opt_dump_list)


def dump_load_dbs(SOURCE, CLONE, args_array, req_rep_cfg, opt_arg_list,
                  **kwargs):

    """Function:  dump_load_dbs

    Description:  Dumps and loads all databases in a single transaction.

    Arguments:
        (input) SOURCE -> Source server instance.
        (input) CLONE -> Destination server instance.
        (input) args_array -> Array of command line options and values.
        (input) req_rep_cfg -> Required replication config settings.
        (input) opt_arg_list -> List of options to add to dump cmd line.
        (input) **kwargs:
            opt_dump_list -> Dictionary of additional options.

    """

    dump_cmd = crt_dump_cmd(SOURCE, args_array, opt_arg_list,
                            kwargs.get("opt_dump_list", []))

    if SOURCE.gtid_mode != CLONE.gtid_mode and not CLONE.gtid_mode \
       and "-n" in args_array and "-r" not in args_array:
        dump_cmd = cmds_gen.is_add_cmd({"-r": "True"}, dump_cmd,
                                       kwargs.get("opt_dump_list", []))

    load_cmd = mysql_libs.crt_cmd(CLONE,
                                  arg_parser.arg_set_path(args_array, "-p") +
                                  "mysql")

    if CLONE.gtid_mode:
        mysql_libs.reset_master(CLONE)

    # Dump databases, pipe into load, and wait until completed.
    P1 = subprocess.Popen(dump_cmd, stdout=subprocess.PIPE)
    P2 = subprocess.Popen(load_cmd, stdin=P1.stdout)
    P2.wait()


def stop_clr_rep(CLONE, args_array, **kwargs):

    """Function:  stop_clr_rep

    Description:  Suspends the slave on the Clone and clears the replication
        configuration if this is for a clone only system.

    Arguments:
        (input) CLONE -> Server instance.
        (input) args_array -> Array of command line options and values.

    """

    if mysql_class.show_slave_stat(CLONE):
        mysql_class.slave_stop(CLONE)

        if "-n" in args_array:
            CLONE.sql("reset slave all")


def chk_rep_cfg(SOURCE, CLONE, args_array, req_rep_cfg, opt_arg_list,
                **kwargs):

    """Function:  chk_rep_cfg

    Description:  Replication configuration check on the source & clone
        servers.

    Arguments:
        (input) SOURCE -> Source server instance.
        (input) CLONE -> Destination server instance.
        (input) args_array -> Array of command line options and values.
        (input) req_rep_cfg -> Required replication config settings.
        (input) opt_arg_list -> List of options to add to dump cmd line.

    """

    if "-n" not in args_array:
        SOURCE.upd_mst_rep_stat()
        CLONE.upd_slv_rep_stat()

        # Both servers meet rep config requirements.
        if not cfg_chk(SOURCE.fetch_mst_rep_cfg, req_rep_cfg["master"]) \
           or not cfg_chk(CLONE.fetch_slv_rep_cfg, req_rep_cfg["slave"]):

            cmds_gen.disconnect(SOURCE, CLONE)
            sys.exit("Error: Master and/or Slave rep config did not pass.")

        if CLONE.gtid_mode:
            # Exclude "change master to"option from dump file.
            opt_arg_list.append("--master-data=2")

        else:
            # Include "change master to" option in dump file.
            opt_arg_list.append("--master-data=1")

    else:
        # Exclude "change master to" option from dump file.
        opt_arg_list.append("--master-data=2")

    return opt_arg_list


def chk_slv_err(MASTER, SLAVE, **kwargs):

    """Function:  chk_slv_err

    Description:  Check the Slave's IO and SQL threads for errors.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).

    """

    if SLAVE:

        for slv in SLAVE:

            io, sql, io_msg, sql_msg, io_time, sql_time = slv.get_err_stat()
            name = slv.get_name()

            # Is there a IO error
            if io:
                print("\nSlave:\t{0}".format(name))
                print("IO Error Detected:\t{0}".format(io))
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


def chk_slv_thr(MASTER, SLAVE, **kwargs):

    """Function:  chk_slv_thr

    Description:  Checks the status of the Slave(s) IO and SQL threads.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).

    """

    if SLAVE:

        for slv in SLAVE:
            thr, io_thr, sql_thr, run = slv.get_thr_stat()
            name = slv.get_name()

            # Check slave IO state and slave running attributes.
            if not thr or not gen_libs.is_true(run):
                print("\nSlave: {0}".format(name))
                print("Error:  Slave IO/SQL Threads are down.")

            # Check slave IO running attribute.
            elif not gen_libs.is_true(io_thr):
                print("\nSlave: {0}".format(name))
                print("Error:  Slave IO Thread is down.")

            # Check slave SQL running attribute.
            elif not gen_libs.is_true(sql_thr):
                print("\nSlave: {0}".format(name))
                print("Error:  Slave SQL Thread is down.")

    else:
        print("\nchk_slv_thr:  Warning:  No Slave instance detected.")


def chk_mst_log(MASTER, SLAVE, **kwargs):

    """Function:  chk_mst_log

    Description:  Compares the binary log and position between the master and
        slave(s) and also compares the read and execute positions of
        the log on the slave itself.

    Arguments:
        (input) MASTER -> Master class instance.
        (input) SLAVE -> Slave class instance(s).

    """

    if MASTER and SLAVE:
        fname, log_pos = MASTER.get_log_info()

        for slv in SLAVE:
            mst_file, relay_file, read_pos, exec_pos = slv.get_log_info()
            name = slv.get_name()

            # If master's log file or position doesn't match slave's log info.
            if fname != mst_file or log_pos != read_pos:

                print("\nWarning:  Slave lagging in reading master log.")
                print("Master: {0}".format(MASTER.name))
                print("\tMaster Log: {0}".format(fname))
                print("\t\tMaster Pos: {0}".format(log_pos))
                print("Slave: {0}".format(name))
                print("\tSlave Log: {0}".format(mst_file))
                print("\t\tSlave Pos: {0}".format(read_pos))

            # 21-04-2020
            # Code is commented out as there is no Chk_Slv to call.
            #  Checking past versions to find out what this did.
            # 11-05-2020
            # Check in mysql_rep_admin.chk_slv.  Will need to bring this
            #   across to this program.
            # Chk_Slv(slv, **kwargs)

    elif SLAVE:
        print("\nchk_mst_log:  Warning:  Missing Master instance.")

        for slv in SLAVE:
            mst_file, relay_file, read_pos, exec_pos = slv.get_log_info()
            name = slv.get_name()

            # 21-04-2020
            # Code is commented out as there is no Chk_Slv to call.
            #  Checking past versions to find out what this did.
            # 11-05-2020
            # Check in mysql_rep_admin.chk_slv.  Will need to bring this
            #   across to this program.
            # Chk_Slv(slv, **kwargs)

    else:
        print("\nchk_mst_log:  Warning:  Missing Master and Slave instances.")


def chk_rep(CLONE, args_array, **kwargs):

    """Function:  chk_rep

    Description:  Create master and slave instances and check the status of the
        replication system between the two servers.

    Arguments:
        (input) CLONE -> Destination server instance.
        (input) args_array -> Array of command line options and values.

    """

    if "-n" not in args_array:
        MASTER = mysql_libs.create_instance(args_array["-c"], args_array["-d"],
                                            mysql_class.MasterRep)

        mysql_libs.change_master_to(MASTER, CLONE)

        SLAVE = mysql_libs.create_instance(args_array["-t"], args_array["-d"],
                                           mysql_class.SlaveRep)
        SLAVE.start_slave()

        # Waiting for slave to start.
        time.sleep(5)
        MASTER.upd_mst_status()
        SLAVE.upd_slv_status()

        chk_slv_err(MASTER, [SLAVE])
        chk_slv_thr(MASTER, [SLAVE])
        chk_mst_log(MASTER, [SLAVE])

        cmds_gen.disconnect(MASTER, SLAVE)


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

    SOURCE = mysql_libs.create_instance(args_array["-c"], args_array["-d"],
                                        mysql_class.Server)
    CLONE = mysql_libs.create_instance(args_array["-t"], args_array["-d"],
                                       mysql_class.Server)

    SOURCE.connect()
    SOURCE.set_srv_gtid()
    CLONE.connect()
    CLONE.set_srv_gtid()

    status, status_msg = mysql_libs.is_cfg_valid([SOURCE, CLONE])

    if not status:
        cmds_gen.disconnect(SOURCE, CLONE)

        for msg in status_msg:
            print(msg)

        sys.exit("Error:  Detected problem in the configuration file.")

    # Do not proceed if GTID modes don't match and rep is being configured.
    if SOURCE.gtid_mode != CLONE.gtid_mode and "-n" not in args_array:
        cmds_gen.disconnect(SOURCE, CLONE)
        sys.exit("Error:  Source (%s) and Clone (%s) GTID modes do not match."
                 % (SOURCE.gtid_mode, CLONE.gtid_mode))

    stop_clr_rep(CLONE, args_array)

    # Add to argument list array based on rep config.
    opt_arg_list = chk_rep_cfg(SOURCE, CLONE, args_array, req_rep_cfg,
                               opt_arg_list)

    print("Starting dump-load process...")
    dump_load_dbs(SOURCE, CLONE, args_array, req_rep_cfg, opt_arg_list,
                  **kwargs)
    print("Finished dump-load process...")

    chk_rep(CLONE, args_array)

    cmds_gen.disconnect(SOURCE, CLONE)


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.

    Variables:
        dir_chk_list -> contains options which will be directories.
        opt_arg_list -> contains arguments to add to command line by default.
        opt_dump_list -> contains optional arguments for mysqldump command.
        opt_req_list -> contains the options that are required for the program.
        opt_val_list -> contains options which require values.
        req_rep_cfg -> contains replication config settings got master/slave.

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    dir_chk_list = ["-d", "-p"]
    opt_arg_list = ["--single-transaction", "--all-databases", "--triggers",
                    "--routines", "--events", "--ignore-table=mysql.event"]
    opt_dump_list = {"-r": "--set-gtid-purged=OFF"}
    opt_req_list = ["-c", "-t", "-d"]
    opt_val_list = ["-c", "-t", "-d", "-p"]
    req_rep_cfg = {"master": {"log_bin": "ON", "sync_binlog": "1",
                              "innodb_flush_log_at_trx_commit": "1",
                              "innodb_support_xa": "ON",
                              "binlog_format": "ROW"},
                   "slave": {"log_bin": "ON", "read_only": "ON",
                             "log_slave_updates": "ON",
                             "sync_master_info": "1", "sync_relay_log": "1",
                             "sync_relay_log_info": "1"}}

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message):
        if not arg_parser.arg_require(args_array, opt_req_list):
            run_program(args_array, req_rep_cfg, opt_arg_list,
                        opt_dump_list=opt_dump_list)


if __name__ == "__main__":
    sys.exit(main())
