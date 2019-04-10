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
