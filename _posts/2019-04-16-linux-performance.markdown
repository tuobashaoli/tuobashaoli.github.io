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
