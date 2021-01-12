---
categories: blog
date: '2021-01-08  10:17:18'
description: keepailved
layout: post
published: True
title: "keepailved and lvs"
---

## 部署


在ubuntu环境中，直接使用`apt-get install keepalived`安装

## 原理

### vrrp协议

虚拟路由器：虚拟路由器是VRRP备份组中所有路由器的集合，它是一个逻辑概念，主路由器+所有备份路由器=虚拟路由器

主路由器： 虚拟路由器通过虚拟IP对外提供服务，而在虚拟路由器内部同一时间只有一台物理路由器对外提供服务，这台提供服务的物理路由器被称为主路由器

备份路由器：虚拟路由器中的其他物理路由器不拥有对外的虚拟IP，也不对外提供网络功能，仅接受MASTER的VRRP状态通告信息，这些路由器被称为备份路由器。当主路由器失败时，处于BACKUP角色的备份路由器将重新进行选举，产生一个新的主路由器进入MASTER角色，继续提供对外服务，整个切换对用户来说是完全透明的。

选举算法：
1.VRRP组中IP拥有者。如果虚拟IP地址与VRRP组中的某台VRRP路由器IP地址相同，则此路由器为IP地址拥有者，这台路由器将被定位主路由器。
2.比较优先级。如果没有IP地址拥有者，则比较路由器的优先级，优先级的范围是0~255，优先级大的作为主路由器
3.比较IP地址。在没有Ip地址拥有者和优先级相同的情况下，IP地址大的作为主路由器。

## 配置

部署keepalived的服务器需要网卡开启多播功能，并且iptables需要允许vrrp多播

```
iptables -A INPUT -p vrrp -j ACCEPT
```

一般关闭防火墙，避免防火墙拦截请求

```
cat /etc/keepalived/keepalived.conf
! Configuration File for keepalived
global_defs {
    router_id lb02 #标识信息，一个名字而已；
}
# 防止脑裂现象，在检查脚本里面检查到nginx服务失败后，停止keepalived服务
vrrp_script check {
    script "/server/scripts/check_list"
    interval  10
}

vrrp_instance VI_1 {
    state MASTER    #角色是master，备份的是BACKUP
    interface eth0  #vip 网卡
    virtual_router_id 50    #让master 和backup在同一个虚拟路由里，id 号必须相同；
    priority 150            #优先级,谁的优先级高谁就是master，备份的比master的要小;
    advert_int 1            #心跳间隔时间
	#nopreempt 将所有的节点都配置BACKUP，并且都开启这个选项，为非抢占模式，即主节点down了再恢复后，不会再抢回MASTER角色
    authentication {
        auth_type PASS      #认证
        auth_pass 1111      #密码
}
    virtual_ipaddress {
        10.0.0.3            #虚拟ip，实际上选取的虚拟ip尽量和选定的网卡中的ip在同一个子网中
    }
	track_script  {
    	check
	}
}
```

默认日志在/var/log/messages文件中

## LVS

### LVS NAT

ipvs运行在iptables中的input链中，对比请求中的ip，转发到postrouting链中，发送给后台真实的ip


缺点：对Director Server压力会比较大，请求和响应都需经过director server


### LVS DR

过为请求报文重新封装一个MAC首部进行转发，源MAC是DIP所在的接口的MAC，目标MAC是某挑选出的RS的RIP所在接口的MAC地址；源IP/PORT，以及目标IP/PORT均保持不变

缺点： RS和DS必须在同一机房中

### LVS Tun

在原有的IP报文外再次封装多一层IP首部，内部IP首部(源地址为CIP，目标IIP为VIP)，外层IP首部(源地址为DIP，目标IP为RIP)

### 调度算法

#### 轮询调度

rr

#### 加权轮询

wrr

#### 原地址hash

sh

#### 目标地址hash

dh

#### 最少连接

lc

#### 加权最短连接

wlc

#### 最短期望延迟

sed

#### 最少队列

nq

#### 基于局部性的最少连接

lblc

#### 带复制的基于局部性最少链接

lblcr

### 配置

配合keepalived，实际上是在keepalived中的添加配置

```
global_defs {
   notification_email {
         edisonchou@hotmail.com
   }
   notification_email_from sns-lvs@gmail.com
   smtp_server 192.168.80.1
   smtp_connection_timeout 30
   router_id LVS_DEVEL  # 设置lvs的id，在一个网络内应该是唯一的
}
vrrp_instance VI_1 {
    state MASTER   #指定Keepalived的角色，MASTER为主，BACKUP为备 记得大写
    interface eno16777736  #网卡id 不同的电脑网卡id会有区别 可以使用:ip a查看
    virtual_router_id 51  #虚拟路由编号，主备要一致
    priority 100  #定义优先级，数字越大，优先级越高，主DR必须大于备用DR
    advert_int 1  #检查间隔，默认为1s
    authentication {   #这里配置的密码最多为8位，主备要一致，否则无法正常通讯
        auth_type PASS
        auth_pass 1111
    }
    virtual_ipaddress {
        192.168.1.200  #定义虚拟IP(VIP)为192.168.1.200，可多设，每行一个
    }
}
# 定义对外提供服务的LVS的VIP以及port
virtual_server 192.168.1.200 80 {
    delay_loop 6 # 设置健康检查时间，单位是秒
    lb_algo rr # 设置负载调度的算法为wlc
    lb_kind DR # 设置LVS实现负载的机制，有NAT、TUN、DR三个模式
    nat_mask 255.255.255.0
    persistence_timeout 0
    protocol TCP
    real_server 192.168.1.130 80 {  # 指定real server1的IP地址
        weight 3   # 配置节点权值，数字越大权重越高
        TCP_CHECK {
        connect_timeout 10
        nb_get_retry 3
        delay_before_retry 3
        connect_port 80
        }
    }
    real_server 192.168.1.131 80 {  # 指定real server2的IP地址
        weight 3  # 配置节点权值，数字越大权重越高
        TCP_CHECK {
        connect_timeout 10
        nb_get_retry 3
        delay_before_retry 3
        connect_port 80
        }
     }
}
```

注意，如果使用DR的LVS负载机制，就需要在转发的nginx服务器上，添加lo网络接口多播的虚拟ip监听，开启的脚本如下，执行`bash functions start`,启动后，就可以再看lo网络接口中监听192.168.1.200的请求了，

```
#虚拟的vip 根据自己的实际情况定义
SNS_VIP=192.168.1.200
/etc/rc.d/init.d/functions
case "$1" in
start)
       ifconfig lo:0 $SNS_VIP netmask 255.255.255.255 broadcast $SNS_VIP
       /sbin/route add -host $SNS_VIP dev lo:0
       echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore
       echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce
       echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
       echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce
       sysctl -p >/dev/null 2>&1
       echo "RealServer Start OK"
       ;;
stop)
       ifconfig lo:0 down
       route del $SNS_VIP >/dev/null 2>&1
       echo "0" >/proc/sys/net/ipv4/conf/lo/arp_ignore
       echo "0" >/proc/sys/net/ipv4/conf/lo/arp_announce
       echo "0" >/proc/sys/net/ipv4/conf/all/arp_ignore
       echo "0" >/proc/sys/net/ipv4/conf/all/arp_announce
       echo "RealServer Stoped"
       ;;
*)
       echo "Usage: $0 {start|stop}"
       exit 1
esac
exit 0
```

