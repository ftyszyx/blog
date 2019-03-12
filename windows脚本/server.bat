rem 添加用户并且创建用户私有目录
set username=
set /p username=input username:
set folderpath=D:\%username%
NET USER %username% 123456 /add /comment:"Example Account for User" /expires:never  
net localgroup "Remote Desktop Users" %username% /add

if exist %folderpath% (
	echo "folder exit"
	) else (
		md %folderpath%
		echo y|cacls.exe d:\%username% /c /e /t /r users
		echo y|cacls.exe d:\%username% /c /e /t /p %username%:f
	)


NET USER %username%  /HOMEDIR:D:\%username%