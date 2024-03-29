# 校园网固件定制
## 固件说明：LEDE有默认设定，无需进行固件基础的初始化操作，直接选择插件源码编译即可。
---
## openwrt官方原版固件编译初始化
## 准备工作
1. 准备好装好ubuntu系统的虚拟机，版本选ubuntu的最新版即可
2. 给ubuntu系统装好vm-tools工具（[教程](https://jingyan.baidu.com/article/d169e18601b381436611d8c8.html)）
3. 更换ubuntu系统软件源，打开软件和更新界面，选择下载至其他站点，选中中国阿里源，也可直接修改源文件（[教程](https://blog.csdn.net/qq_35451572/article/details/79516563)）
4. 准备好虚拟机共享文件夹（[教程](https://jingyan.baidu.com/article/f79b7cb38e5391d144023ead.html)）
5. 准备好全局梯子，需要保证终端墙外网络畅通
6. 准备好需要编译的插件源码
7. 准备好OpenWrt的官方固件源码包，使用OpenWrt源码分支[18.06.8](https://github.com/openwrt/openwrt/archive/v18.06.8.tar.gz)版本
8. 把OpenWrt的固件源码包解压到ubuntu系统主目录下，不可放在桌面
---
## 部署虚拟机环境
- ### 更新ubuntu系统软件
    `sudo apt-get update && sudo apt-get -y upgrade && sudo apt autoremove`
- ### 安装OpenWrt依赖
    `sudo apt-get install -y gcc g++ binutils patch bzip2 flex bison make autoconf gettext texinfo unzip sharutils subversion libncurses5-dev ncurses-term zlib1g-dev subversion git-core gawk asciidoc libz-dev zlib1g-dev libssl-dev openssl`
---
## 相关编译命令——需要把当前目录切换到源码包下操作
- ### 下载OpenWrt软件包
    `./scripts/feeds update -a && ./scripts/feeds install -a`
- ### 定制固件菜单
    `make menuconfig`
- ### 清除固件菜单配置，恢复成默认配置
    `rm -f .config && rm -f .config.old`
- ### 开始编译命令
    `make V=99`
---
## 固件菜单选择——官方OpenWrt编译菜单必选
- 添加luci (web界面管理)`LuCI->Collections->luci`
- 添加中文语言包`LuCI->Module->translation->chinese`
- 添加默认主题`LuCI->Themes->luci-theme-material`
---
## 修改OpenWrt源码默认配置
- ### WiFi相关设置——`package/kernel/mac80211/files/lib/wifi/mac80211.sh`
    - #### 开启WiFi
        ```diff
        - option disabled 1
        + option disabled 0
        ```
    - #### 设置WiFi相关参数
        ```diff
        - set wireless.default_radio${devidx}.encryption=none
        # 设置WiFi加密方式
        + set wireless.default_radio${devidx}.encryption=psk
        # 设置WiFi密码
        + set wireless.default_radio${devidx}.key=12345678
        # 关闭WiFi的wmm和剔除弱信号
        + set wireless.default_radio${devidx}.wmm=0
        + set wireless.default_radio${devidx}.disassoc_low_ack=0
        ```
- ### 修改用户登录的默认密码为admin——`package/base-files/files/etc/shadow`
    ```diff
    - root::0:0:99999:7:::
    + root:$1$wEehtjxj$YBu4quNfVUjzfv8p/PBo5.:0:0:99999:7:::
    ```
- ### 修改默认语言为中文——`feeds/luci/modules/luci-base/root/etc/config/luci`
    ```diff
    - option lang auto
    + option lang zh_cn
    ```
- ### 修改时区——`package/base-files/files/bin/config_generate`
    ```diff
    - set system.@system[-1].timezone='UTC'
    + set system.@system[-1].timezone='CST-8'
    + set system.@system[-1].zonename='Asia/Shanghai'
    ```
- ### 添加计划任务——`package/base-files/files/etc/crontabs/root`
    把crontabs文件夹放到源码`package/base-files/files/etc`下
- ### 添加开机自启动任务（可选）——`package/base-files/files/etc/rc.local`
---
## 校园网专属固件定制
- ### 编译菜单选择自动登录、破解限制——把插件源码放在源码package目录下
    - `Languages->Python->python-autologin`
    - `Kernel modules->Other modules->kmod-xmurp-ua`
---
## 其他
- ### 优酷路由宝WiFi灯控制
    - 开`echo 1 > /sys/class/leds/youku-yk1\:blue\:air/brightness`
    - 关`echo 0 > /sys/class/leds/youku-yk1\:blue\:air/brightness`
- ### UA过滤生效后，防火墙设置流量放行
    - #### 放行特定条件的目标
        - `iptables -t mangle -A PREROUTING -s 192.168.1.126 -j MARK --set-mark 1`
        - `iptables -t mangle -A PREROUTING -d httpbin.org -j MARK --set-mark 1`
        - `iptables -t mangle -A PREROUTING -p tcp --dport 80 -m mac --mac-source 80:FA:5B:40:59:03 -j MARK --set-mark 1`
    - #### 放行所有80上行tcp数据包
        `iptables -t mangle -A PREROUTING -p tcp -m tcp --dport 80 -j MARK --set-mark 1`