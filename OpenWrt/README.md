Python3 完成校园网认证
=====================

版本说明：<br>
---------------------
    1、三个版本都可以用于自动登录城院校园网。虽然他们都是用python实现，但是python中有python2也有python3，他们的一些差异导致每个版本适用性不一样。
    2、在openwrt（lede）中，推荐使用urllib和urllib2实现那个版本。因为在openwrt里面，python2比较成熟，而python3发展的还不是特别好，所以得要用推荐的那个版本才能在openwrt（lede）中正常运行。
    3、如果是在PC下面跑，需要稍微改动下源码。推荐用urllib那个版本，当然你的环境得是python3，python2的话看着来挑；选择requests也行，不过requests属于第三方库，需要安装。
    4、三个版本的使用方法虽然不同，但是其实现原理是一模一样，只是换了条裤子。

适用环境：<br>
---------------------
    python2.7（OpenWrt、LEDE）。
交叉编译需知：<br>
--------------------
    以lean大的LEDE固件（https://github.com/coolsnowwolf/lede）为例，由于程序并没有加入luci控制界面，所以需要手动设置开机自启动和计划任务，为了方便以后再编译使用，我修改了lean的默认配置default-settings（），加入了以下代码：
    # 自启动代码
    sed -i '/exit 0/i/usr/sbin/autologin 学号 密码 天翼账号 密码' /etc/rc.local

    # 计划任务代码
    mkdir -p /etc/crontabs
    echo -e '30 6 * * * reboot\n*/5 * * * * /usr/sbin/autologin 学号 密码 天翼账号 天翼密码' >> /etc/crontabs/root
