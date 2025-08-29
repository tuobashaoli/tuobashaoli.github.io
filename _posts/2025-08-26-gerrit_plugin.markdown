---
categories: blog
date: '2025-08-26 21:29:18'
description: gerrit插件开发
layout: post
published: True
title: "gerrit插件开发"
tags: gerrit
---


# 准备环境

首先是外网连接权限，这个是大前提，如果你使用的是公司的网络，大概率就没这个问题，毕竟，使用公司网络是合法的，🐶

官方的插件都是在网站`https://gerrit-ci.gerritforge.com/`上面编译发布的，如果想知道编译的环境，直接从官网上查看日志就可以了

![avatar](/assets/images/gerrit_checks_build.png)

比如上图，看出来需要jdk21 和 bazel 7.2.1,那么就去安装这个环境

```shell
sudo apt install openjdk-21-jdk-headless
```

安装bazel的方式在官网上`https://bazel.build/install/ubuntu?hl=zh-cn`

```shell
wget https://github.com/bazelbuild/bazel/releases/download/7.2.1/bazel-7.2.1-installer-linux-x86_64.sh
chmod +x bazel-7.2.1-installer-linux-x86_64.sh
./bazel-7.2.1-installer-linux-x86_64.sh --user
export PATH="$PATH:$HOME/bin"
```


# 下载gerrit代码

```shell
 # 下载整个gerrit的代码
 git clone "https://gerrit.googlesource.com/gerrit" gerrit2
 cd gerrit2
 # 注意一定要下载submodule，否则就会有奇怪的报错
 git submodule update --init --recursive
```

# 下载需要编译的插件的代码

这里用官方的checks插件为例，进行编译

```shell
git clone https://gerrit.googlesource.com/plugins/checks
# 把插件代码复制到gerrit仓库源码的plugins目录里面
cp -r checks gerrit2/plugins/

```

# 开始编译

```shell
cd gerrit2
bazel build //plugins/checks:checks
```

我在wsl里面进行编译的，这里报错缺少zip工具，那么我就安装一个zip工具继续编译

![avatar](/assets/images/gerrit_plugin_build.png)


终成正果，阿弥陀佛 ✔

![avatar](/assets/images/gerrit_plugin_build_pass.png)


# checks插件

checks插件是官方提供的前后端都一起剩下的插件，理解了这个插件，就基本掌握了gerrit的插件开发

首先看一下官方画的大饼

`https://gerrit-review.googlesource.com/Documentation/pg-plugin-checks-api.html`


![avatar](/assets/images/user-checks-overview.png)


这里的功能包括

1. 和标签比如Code-Style联动，检查项失败标签自动-1
2. 展示失败详情和链接，这个链接可以是自定义的具体CI上的检查详情
3. 红色表示失败，黄色表示告警，绿色表示成功，灰色表示等待或运行，蓝色表示有信息，展示各个检查项的状态
4. 可以点击重试
5. 可以给各类检查结果贴上标签
6. 可以展示大文本，用于描述检查项更具体的信息


但是，上面的这么多功能，目前的checks插件里面没有使用起来，官方只是在上面这个截图上演示一下而已，实际的代码中，很多功能都没被用上