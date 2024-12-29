@echo off
@setlocal enabledelayedexpansion
pip install build
python -m build

for /f "delims=" %%a in ('call read_ini.bat conf.ini build_info VERSION') do (
    set val=%%a
)
echo %val%

set installFile="dist\slowedreverb-!val!.tar.gz"

pip install %installFile%