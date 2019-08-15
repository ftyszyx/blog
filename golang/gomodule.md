 需要先设置 GO111MODULE 环境变量
 GO111MODULE=on

 初始化：
 go mod init helloworld

 引入库：
 go mod edit -require github.com/cnwyt/mytest@latest

 直接
 go build
 就会下载相应的模块

 ![命令](../static/gomod1.png)