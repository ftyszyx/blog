deepin.md

一、安装ssh:

1.安装登陆服务端
sudo apt-get install openssh-server
2.配置端口
sudo gedit /etc/ssh/sshd_config
3.配置完要重启SSH服务端
sudo /etc/init.d/ssh start 或者 service ssh start

重启ssh服务
service sshd restart


二、可以设置启动模式
设置启动模式：
# 将默认级别修改为多用户文本模式
systemctl set-default multi-user.target
# 将默认级别修改为图形用户界面模式
systemctl set-default graphical.target
# 重启
reboot

三、安装docker:
更新源
sudo apt-get update
添加docker源
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs)  stable"
安装docker
sudo apt-get install docker-ce
测试docker有没有安装成功
sudo docker run hello-world