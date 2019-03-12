rem 添加用户并且创建用户私有目录
set username=
set nickname=
if "%1"==="csv"(
	set list="user.csv"
	for %%i in (%list%) do (
    echo config = %%i 
    for /f "tokens=1-3 delims=," %%a in (%%i) do (
	        echo 学号=%%a 名称=%%b 成绩=%%c
	    )
	)
	)else(
	set /p username=input username:
	set folderpath=D:\%username%
	)



pause


:adduser
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
goto:eof