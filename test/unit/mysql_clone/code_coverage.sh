#!/bin/bash
# Unit test code coverage for program module.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#   that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=mysql_clone test/unit/mysql_clone/cfg_chk.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/chk_mst_log.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/chk_rep.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/chk_rep_cfg.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/chk_slv.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/chk_slv_err.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/chk_slv_thr.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/crt_dump_cmd.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/dump_load_dbs.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/help_message.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/main.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/run_program.py
coverage run -a --source=mysql_clone test/unit/mysql_clone/stop_clr_rep.py

echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
