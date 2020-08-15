# 城院校园网web认证自动登录

## 测试环境：
    coolsnowwolf的LEDE固件

## 各版本说明：
1. urllib和urllib2实现----->python2
2. urllib实现----->python3
3. requests实现----->python2/python3，需额外安装requests库

## 使用方法：
编译coolsnowwolf的LEDE固件时修改[default-settings](https://github.com/Subdue0/CCDGUTNetAutoLogin/releases/download/default-settings%EF%BC%88OpenWrt%EF%BC%89/default-settings.rar)文件

## 在原有default-settings文件中加入以下代码：
    # 程序自启动代码
    sed -i '/exit 0/i/usr/sbin/autologin 学号 密码 天翼账号 密码' /etc/rc.local

    # 计划任务代码
    mkdir -p /etc/crontabs
    echo -e '30 6 * * * reboot\n*/5 * * * * /usr/sbin/autologin 学号 密码 天翼账号 天翼密码' >> /etc/crontabs/root
