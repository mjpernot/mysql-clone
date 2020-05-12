#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
test/unit/mysql_clone/cfg_chk.py
test/unit/mysql_clone/chk_mst_log.py
test/unit/mysql_clone/chk_rep.py
test/unit/mysql_clone/chk_rep_cfg.py
test/unit/mysql_clone/chk_slv.py
test/unit/mysql_clone/chk_slv_err.py
test/unit/mysql_clone/chk_slv_thr.py
test/unit/mysql_clone/crt_dump_cmd.py
test/unit/mysql_clone/dump_load_dbs.py
test/unit/mysql_clone/help_message.py
test/unit/mysql_clone/main.py
test/unit/mysql_clone/run_program.py
test/unit/mysql_clone/stop_clr_rep.py
