#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
/usr/bin/python3 test/unit/mysql_clone/cfg_chk.py
/usr/bin/python3 test/unit/mysql_clone/chk_mst_log.py
/usr/bin/python3 test/unit/mysql_clone/chk_rep.py
/usr/bin/python3 test/unit/mysql_clone/chk_rep_cfg.py
/usr/bin/python3 test/unit/mysql_clone/chk_slv.py
/usr/bin/python3 test/unit/mysql_clone/chk_slv_err.py
/usr/bin/python3 test/unit/mysql_clone/chk_slv_thr.py
/usr/bin/python3 test/unit/mysql_clone/connect_chk.py
/usr/bin/python3 test/unit/mysql_clone/crt_dump_cmd.py
/usr/bin/python3 test/unit/mysql_clone/dump_load_dbs.py
/usr/bin/python3 test/unit/mysql_clone/help_message.py
/usr/bin/python3 test/unit/mysql_clone/main.py
/usr/bin/python3 test/unit/mysql_clone/run_program.py
/usr/bin/python3 test/unit/mysql_clone/stop_clr_rep.py
