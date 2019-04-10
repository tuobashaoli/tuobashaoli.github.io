---
categories: blog
date: '2019-04-10 08:47:18'
description: it is for ansible
layout: post
published: True
title: "Ansible it more"
---

# 一、Ansible实践

### 优化速度
##### 1.开启ssh长连接
##### 在/etc/ansible/ansible.cfg中做如下设置，需要ssh版本大于5.6
```cfg
ssh_args = -o ControlMaster=auto -o ControlPersist=5d
```
##### 2.开启pipelining
##### 在ansible.cfg中设置

```cfg
pipelining = True
```

##### 3.开启accelerate模式
##### 需要在控制机和被控制机都要安装python-keyczar软件包，然后在playbook中设置

```cfg
accelerate: true
```

##### 4.设置facts缓存
##### 在ansible.cfg中设置如下

```cfg
gathering = smart
fact_caching_timeout = 86400
fact_caching = jsonfile
fact_caching_connection = /dev/shm/ansible_fact_cache
```

### ansible-shell

##### ansible-shell并非是ansible默认工具，需要额外安装,工具信息在[这里](https://github.com/dominis/ansible-shell.git)，只支持Ad-Hoc命令，可以使用tab进行命令补齐

# 二、扩展ansible组件

### 扩展facts
##### 当前的fact信息都是机器本身的硬件或者软件信息，和机器所承担的服务无法直接区分
##### 机器的fact信息是通过setup模块收集的，Facts类下，有个facts.py 文件，其中get\_local\_facts函数用户收集ansible\_local信息。在modules/core/system/setup.py中可以看到，fact\_path默认是/etc/ansible/facts.d，也就是说，在这个目录下的所有.fact文件豆浆被setup模块收集到facts信息中，所以只要在被控制机的该目录下填写.fact文件，格式可以使json或者ini，就可以被收集用于区分主机
##### 但是，这样需要在被控制机中一个一个去写信息，还是比较麻烦，但是，修改fact信息采集方式，就不必这么麻烦了
