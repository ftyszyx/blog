android逆向
参考：
https://juejin.im/post/5ae2ddfe51882567113aee21


1、apktook解压包，
2、可以用smail2java工具，全翻译成java代码，对照java代码，
https://github.com/pxb1988/dex2jar 将dex变成jar
然后用jd-gui生成Java
修改包中的smail文件（代码）

3、用apktoo将smail文件生成dex文件，并打出未签名包
apktool -b apk/

4、对包进行签名


5、签名的破解参考
https://blog.upx8.com/1418