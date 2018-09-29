@echo off
title 加入或删除程序开机自启
color 0a
mode 58,26


:menu
cls

echo.

echo                                 !\___/！ 
echo                                 ! ●x● 
echo                      ╭ .  _____ノ  ︶/ 
echo                       \＼/    /、   丿      
echo                       ＼ __ ____   ノ         
echo                        (/  \)  (/ヽ)          
echo                ￣￣￣￣￣￣￣￣￣￣￣￣￣￣    
echo                         作者:Subdue

echo                      时间：2018年9月25日

echo.

if exist "C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\autologin.exe" (
choice /m 校园网自动登录程序已加入开机自启，如果你要删除自启动请按：Y，退出请按：N
if errorlevel 2 goto exit
if errorlevel 1 goto del
) else (
choice /m 检测到校园网自动登录程序没有加入开机自启，如果你需要程序开机自启动请按：Y，退出请按：N
if errorlevel 2 goto exit
if errorlevel 1 goto move
)


:move
cls
if exist "C:\Users\%username%\Desktop\autologin.exe" (
move "C:\Users\%username%\Desktop\autologin.exe" "C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
choice /m 开机自启已加入，返回主界面请按：Y，退出请按：N
if errorlevel 2 goto exit
if errorlevel 1 goto menu
) else (
choice /m 桌面的autologin.exe文件不存在，返回主界面请按：Y，退出请按：N
if errorlevel 2 goto exit
if errorlevel 1 goto menu
)


:del
cls
if exist "C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\autologin.exe" (
del "C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\autologin.exe"
choice /m 开机自启已删除，返回主界面请按：Y，退出请按：N
if errorlevel 2 goto exit
if errorlevel 1 goto menu
) else (
choice /m 程序没有加入开机自启，返回主界面请按：Y，退出请按：N
if errorlevel 2 goto exit
if errorlevel 1 goto menu
)


:exit
