git clone 加速

全局代理：
git config --global http.proxy socks5://127.0.0.1:1080
git config --global https.proxy socks5://127.0.0.1:1080
取消：
git config --global --unset http.proxy
git config --global --unset https.proxy
只针对部分域名代理（推荐）

git config --global http.https://github.com.proxy socks5://127.0.0.1:1080
git config --global https.https://github.com.proxy socks5://127.0.0.1:1080
