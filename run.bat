echo off
python run.py

setlocal enabledelayedexpansion

rem �����ļ�����Ŀ¼
set src_dir=.\result

rem filename���ڴ��Ŀ���ļ���
set filename=""

cd /d %src_dir%
for /f %%a in ('dir /o-d /tc /b') do (
    echo �ļ�������Ϣ: %%a
    set filename=%%~na%%~xa
    echo �ļ���: !filename!, ���´���ʱ�䣺 %%~ta
    if not !filename! == ""  (
        goto allurecmd
    )
)

:allurecmd
allure generate ./!filename!/report/xml -o ./!filename!/report/html

cmd
