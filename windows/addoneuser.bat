@echo off

set username=ljl
set nickname=½����
set password=641524

set folderpath=D:\˽��Ŀ¼\%nickname%
NET USER %username% %password% /add /comment:"Account for User" /expires:never  
net localgroup "Remote Desktop Users" %username% /add

if exist %folderpath% (
	echo "folder exit"
	) else (
		md %folderpath%
		echo y|cacls.exe %folderpath% /c /e /t /r users
		echo y|cacls.exe %folderpath% /c /e /t /p %username%:f
	)


set folderpath2=D:\�ɶ�˽��Ŀ¼\%nickname%
if exist D:\�ɶ�˽��Ŀ¼\%nickname% (
echo "folder exit"
) else (
	md D:\�ɶ�˽��Ŀ¼\%nickname%
	echo y|cacls.exe D:\�ɶ�˽��Ŀ¼\%nickname%  /c /e /t /p users:r
	echo y|cacls.exe D:\�ɶ�˽��Ŀ¼\%nickname% /c /e /t /p %username%:f
)
NET USER %username%  /HOMEDIR:%folderpath%
