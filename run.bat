echo off
python run.py

setlocal enabledelayedexpansion

rem 设置文件所在目录
set src_dir=.\result

rem filename用于存放目标文件名
set filename=""

cd /d %src_dir%
for /f %%a in ('dir /o-d /tc /b') do (
    echo 文件完整信息: %%a
    set filename=%%~na%%~xa
    echo 文件名: !filename!, 最新创建时间： %%~ta
    if not !filename! == ""  (
        goto allurecmd
    )
)

:allurecmd
allure generate ./!filename!/report/xml -o ./!filename!/report/html

cmd
