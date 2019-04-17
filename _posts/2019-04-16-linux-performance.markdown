---
categories: blog
date: '2019-04-16 20:10:18'
description: how to know performance of linux machine
layout: post
published: True
title: "linux performance command"
---

# linux性能信息获取的shell命令

### CPU

##### vmstat

间隔2秒，输出3次
`vmstat 2 3`

![avatar](/assets/images/vmstat.png)

```
procs  r  运行队列中进程的数量
       b  等待io的进程数
memory swpd  使用虚拟内存大小
       free  空闲的物理内存
       buff  缓冲区，用于存放要输出到磁盘的的数据
       cache 页高速缓存，存放从磁盘上取出的数据，如果值较大，那么磁盘io bi就会比较小
swap   si  每秒从交换区写到内存的大小
       so  每秒写入交换区的大小
       如果这俩个值长期大于0,说明内存不足
io     bi  每秒读取的块数
       bo  每秒写入的块数
       如果这俩个值越大，则cpu在io等待的值也就越大
system in  每秒中断数
       cs  每秒上下文切换数
       如果这俩个值较大，则内核消耗的cpu时间就会大
cpu    us  用户进程执行时间的百分比
       sy  内核系统进程执行时间的百分比
       wa  io等待时间百分比，值较大，说明io等待严重，可能出现磁盘访问瓶颈
       id  空闲时间百分比
       st  虚拟机偷取的CPU所占的百分比
```

##### sar
需要安装sysstat。
在多核cpu的系统中，cpu整体使用率不高，但是系统响应缓慢，可能时单线程只是用一个cpu导致，使用sar命令


`sar -P 0 3 5` 第一个cpu，每隔3秒打印占用率情况
![avatar](/assets/images/sar.png)

```
%nice 已调整优先级的用户进程的CPU时间
```

##### uptime

显示1、5、15分钟内运行队列的平均进程数，如果一个进程满足以下条件则会位于运行队列中

+ 没有等待IO操作
+ 没有主动进入等待状态
+ 没有被停止

### 内存性能评估

##### free

`free -h` 以方便查看的单位显示内存使用情况

##### sar

`sar -r 1`每隔一秒输出一次内存占用情况

```
kbmemfree 和free的free基本一致，不包括buffer和cache
kbmemused 和free的used基本一致，包括buffer和cache
%memused kbmemused和内存总量(不包括swap)的一个百分比
kbbuffers和kbcached  就是free命令中的buffer和cache
kbcommit 保证当前系统所需要的内存
%commit 这个值是kbcommit与内存总量(包括swap)的一个百分比
```

### 磁盘IO性能评估

`sar -d 1 -p` 每隔一秒打印块设备的io信息

![avatar](/assets/images/sar-d.PNG)

```
tps 每秒从物理磁盘IO的次数
rd_sec/s 每秒读扇区的次数
wr_sec/s 每秒写扇区的次数
avgrq-sz 平均每次设备io操作的数据大小，以扇区为单位
avgqu-sz 磁盘请求队列的平均长度
await 从请求磁盘操作到系统完成处理，每次请求的平均消耗时间，包括请求队列的等待时间，单位是毫秒
svctm 系统处理每次请求的平均时间，不包括在请求队列中消耗的时间，当svctm接近await的时候，说明几乎没有等待时间，IO性能很好
%util IO请求占CPU百分比，越大，说明越饱和
```

`iostat -d 1`


### 网络性能评估

`sar -n DEV|EDEV|SOCK|FULL 2 3` 查看网络接口\|网络错误统计\|套接字\|所有信息，每个2每秒打印一次，打印3次


```
IFACE 网络接口
rxpck/s 每秒钟接收的数据包
txpck/s 每秒钟发送的数据包
rxkB/s 每秒钟接收的字节数
txkB/s 每秒钟发送的字节数
rxcmp/s 每秒钟接收的压缩数据包
txcmp/s 每秒中发送的压缩数据包
rxmcst/s 每秒钟接收的多播数据包
%ifutil
```

`nslookup  www.baidu.com`查看www.baidu.com的ip地址

`netstat -tunlp` 以数字numeric形式显示tcp和udp报文，并显示监听端口和pid
