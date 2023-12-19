@echo off
cd /d %~dp0
python paper_list.py
set https_proxy=127.0.0.1:7890
git add *
git commit -m %DATE:~0,4%_%DATE:~5,2%_%DATE:~8,2%——%TIME:~0,2%_%TIME:~3,2%_%TIME:~6,2%
git pull
git push