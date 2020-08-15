城院校园网认证
=====================

版本说明：<br>
---------------------
    1、三个版本都可以用于自动登录城院校园网。虽然他们都是用python实现，但是python中有python2也有python3，他们的一些差异导致每个版本适用性不一样。
    2、在openwrt（lede）中，推荐使用urllib和urllib2实现那个版本。因为openwrt中，python2支持的第三方库比较多。
    3、如果是在PC下面跑，需要稍微改动下源码。推荐用urllib那个版本，当然你的环境得是python3，python2的话看着来挑；选择requests也行，不过requests属于第三方库，需要安装。
    4、三个版本的使用方法虽然不同，但是其实现原理是一模一样，区别在于实现库不同。

适用环境：<br>
---------------------
    python2.7（OpenWrt、LEDE）。
编译coolsnowwolf的LEDE时修改default-settings：<br>
--------------------
    https://github.com/Subdue0/CCDGUTNetAutoLogin/releases/download/default-settings%EF%BC%88OpenWrt%EF%BC%89/default-settings.rar
在原有default-settings文件中加入以下代码：<br>
--------------------
    # 自启动代码
    sed -i '/exit 0/i/usr/sbin/autologin 学号 密码 天翼账号 密码' /etc/rc.local

    # 计划任务代码
    mkdir -p /etc/crontabs
    echo -e '30 6 * * * reboot\n*/5 * * * * /usr/sbin/autologin 学号 密码 天翼账号 天翼密码' >> /etc/crontabs/root
