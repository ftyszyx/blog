@echo off

set username=ljl
set nickname=Â½½àÀ¼
set password=641524

set folderpath=D:\Ë½ÓÐÄ¿Â¼\%nickname%
NET USER %username% %password% /add /comment:"Account for User" /expires:never  
net localgroup "Remote Desktop Users" %username% /add

if exist %folderpath% (
	echo "folder exit"
	) else (
		md %folderpath%
		echo y|cacls.exe %folderpath% /c /e /t /r users
		echo y|cacls.exe %folderpath% /c /e /t /p %username%:f
	)


set folderpath2=D:\¿É¶ÁË½ÓÐÄ¿Â¼\%nickname%
if exist D:\¿É¶ÁË½ÓÐÄ¿Â¼\%nickname% (
echo "folder exit"
) else (
	md D:\¿É¶ÁË½ÓÐÄ¿Â¼\%nickname%
	echo y|cacls.exe D:\¿É¶ÁË½ÓÐÄ¿Â¼\%nickname%  /c /e /t /p users:r
	echo y|cacls.exe D:\¿É¶ÁË½ÓÐÄ¿Â¼\%nickname% /c /e /t /p %username%:f
)
NET USER %username%  /HOMEDIR:%folderpath%
