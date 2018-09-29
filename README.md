Python3 完成校园网认证
=====================

程序有效期：<br>
------------------
    止于校园网再度升级
需要模块：<br>
--------------------
    requests, pillow
适用学校：<br>
---------------------
    仅适用东莞理工学院城市学院
适用环境：<br>
---------------------
    Win10，Win7测试均通过，Mac未测试
使用方法 ：<br>
--------------------
    首先下载压缩包：https://github.com/Subdue0/CCDGUTNetAutoLoginW/releases/download/v1.0/CCDGUTAutoLogin.rar
    
    然后，解压exe，bat，txt三个类型的文件到你的桌面上；
    
    然后，编辑info.txt里面的数据，改成相应的账号密码以及更改默认的延迟启动时间（可选择默认）；
    
    接着，运行bat文件，将程序加入开机自启动，再将电脑WiFi中的自动连接打上勾，有线网络不用就禁用掉，如果用有线网络连接，就把WiFi自动连接关掉，避免两种上网方式同时存在；
    
    最后，直接重启电脑。
移植说明：<br>
--------------------
    python最大的优点亦是它最大的缺点，用它所写出的程序所依赖的库非常多，在openwrt里面打包后程序还是蛮大的，这不便于它移植到非常小rom空间的路由器中，但是想要移植也不是不可行的，稍微改动下源码，再把路由器rom空间弄大点就OK。
    
    但是，有更适用于嵌入式设备的C/C++，Python大法还是得靠边站！！！
