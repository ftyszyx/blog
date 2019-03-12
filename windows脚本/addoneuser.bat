@echo off

set username=
set nickname=
set password=

set /p username=input username:
set /p password=input password:

set folderpath=D:\%username%
NET USER %username% %password% /add /comment:"Account for User" /expires:never  
net localgroup "Remote Desktop Users" %username% /add

if exist %folderpath% (
	echo "folder exit"
	) else (
		md %folderpath%
		echo y|cacls.exe %folderpath% /c /e /t /r users
		echo y|cacls.exe %folderpath% /c /e /t /p %username%:f
	)


NET USER %username%  /HOMEDIR:%folderpath%
