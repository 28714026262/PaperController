cd /d %~dp0
python paper_list.py
set https_proxy=127.0.0.1:7890
git add *
git commit -m %date:~6,4%-%date:~0,2%-%date:~3,2%
git pull
git push