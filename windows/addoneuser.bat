@echo off

set username=ljl
set nickname=陆洁兰
set password=641524

set folderpath=D:\私有目录\%nickname%
NET USER %username% %password% /add /comment:"Account for User" /expires:never  
net localgroup "Remote Desktop Users" %username% /add

if exist %folderpath% (
	echo "folder exit"
	) else (
		md %folderpath%
		echo y|cacls.exe %folderpath% /c /e /t /r users
		echo y|cacls.exe %folderpath% /c /e /t /p %username%:f
	)


set folderpath2=D:\可读私有目录\%nickname%
if exist D:\可读私有目录\%nickname% (
echo "folder exit"
) else (
	md D:\可读私有目录\%nickname%
	echo y|cacls.exe D:\可读私有目录\%nickname%  /c /e /t /p users:r
	echo y|cacls.exe D:\可读私有目录\%nickname% /c /e /t /p %username%:f
)
NET USER %username%  /HOMEDIR:%folderpath%
