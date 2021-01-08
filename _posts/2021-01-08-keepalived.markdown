---
categories: blog
date: '2021-01-08  10:17:18'
description: keepailved
layout: post
published: True
title: "keepailved"
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
        10.0.0.3            #虚拟ip
    }
	track_script  {
    	check
	}
}
```

默认日志在/var/log/messages文件中