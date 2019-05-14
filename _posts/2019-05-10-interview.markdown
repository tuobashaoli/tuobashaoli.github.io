---
title: "interview"
date: "2019-05-10 20:30:18"
layout: post
categories: blog
published: True
---

# futu

### ulimit

ulimit主要是用来限制进程对资源的使用情况的，它支持各种类型的限制，常用的有：

内核文件的大小限制

进程数据块的大小限制

Shell进程创建文件大小限制

可加锁内存大小限制

常驻内存集的大小限制

打开文件句柄数限制

分配堆栈的最大大小限制

CPU占用时间限制用户最大可用的进程数限制

Shell进程所能使用的最大虚拟内存限制

选项 含义

-a 显示当前系统所有的limit资源信息。 

-H 设置硬资源限制，一旦设置不能增加。

-S 设置软资源限制，设置后可以增加，但是不能超过硬资源设置。

-c 最大的core文件的大小，以 blocks 为单位。

-f 进程可以创建文件的最大值，以blocks 为单位.

-d 进程最大的数据段的大小，以Kbytes 为单位。

-m 最大内存大小，以Kbytes为单位。

**-n 查看进程可以打开的最大文件描述符的数量。**

-s 线程栈大小，以Kbytes为单位。

-p 管道缓冲区的大小，以Kbytes 为单位。

**-u 用户最大可用的进程数。**

-v 进程最大可用的虚拟内存，以Kbytes 为单位。

-t 最大CPU占用时间，以秒为单位。

-l 最大可加锁内存大小，以Kbytes 为单位。

可以使用ulimit命令直接修改这些数值，只会在当前用户使用的环境有效，为了让配置永久生效，可以通过修改文件`/etc/security/limits.conf`实现，或者`/etc/sevurity/limits.d/`目录下的文件，或者在用户启动中使用在bash启动脚本中设置修改。

```
# /etc/security/limits.conf
* soft noproc 11000
* hard noproc 11000
* soft nofile 4100
* hard nofile 4100
```

### 批量创建用户并且让用户第一次登录必须修改代码

迫使用户修改密码，使用命令`sudo chage -d0 username`,表示该用户自上次修改密码后的有效期，另一个命令就是`sudo passwd -e username`,让用户的密码立即失效。

```
users=`cat namelist.txt`
for user in $users;
do
  adduser $user --gecos ""  --disabled-password |chpasswd;chage -d0 $user
done
```

### awk将俩个文件中相同的一行拼接

### free输出

### df显示磁盘空间不足，但是du查找不到

某些文件被删除时，inode没有被释放。可能是日志文件在被删除的时候，inode没有被删除。

### /etc/passwd权限位

644 

### 目录的rwx

r：可读权限
w：可写权限
x：可执行权限，可以cd进入

### k8s的pod的实现原理

### docker的原理

# oubo

### 如何在shell中启动jenkins的job

#### 1.使用curl

无参数

```
curl -X POST ${jenkins_url}/job/${job_name}/build --user ${username}:${passwd}
```

使用默认参数

```
curl -X POST ${jenkins_url}/job/${job_name}/build/buildWithParameters  --user ${username}:${passwd}
```

设置参数

```
curl -X POST ${jenkins_url}/job/${job_name}/build/buildWithParameters  -d param1=value1&&param2=value2 --user ${username}:${passwd}
```

#### 2.使用python-jenkins模块

#### 3.使用jenkins CLI

### 如何批量的给jenkins添加节点

#### 使用python-jenkins

假设本机的ssh公钥已经配置到所有节点authorized\_keys中，如果没有，使用`ssh-copy-id -u $username -i ~$username/.ssh/id_rsa.pub $sshusername@$ip`将公钥复制过去
`create_node(name, numExecutors=2, nodeDescription=None, remoteFS='/var/lib/jenkins', labels=None, exclusive=False, launcher='jenkins.LAUNCHER_COMMAND', launcher_params={})`

### 替换文本

`sed -i "s/a/b/g" file`
`cat file|tr a b`
`${path//a/b}``${path/a/b}`

