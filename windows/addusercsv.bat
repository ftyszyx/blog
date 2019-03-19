@echo off


for /f "tokens=1-3 delims=," %%a in  ('type "user.csv"') do (
echo "username"%%a 
echo "nickname"%%b 
echo "password"%%c 
echo "folderpath"D:\%%b

NET USER %%a %%c /add /comment:"Account for User" /expires:never  
net localgroup "Remote Desktop Users" %%a /add

if exist D:\%%b (
echo "folder exit"
) else (
	md D:\%%b
	echo y|cacls.exe D:\%%b  /c /e /t /r users
	echo y|cacls.exe D:\%%b  /c /e /t /p %%a:f
)

NET USER %%a  /HOMEDIR:D:\%%b
)


