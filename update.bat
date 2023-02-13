cd /d %~dp0
python paper_list.py
set https_proxy=127.0.0.1:7890
git add *
set /p declation = %date%
git commit -m %declation%
git pull
git push