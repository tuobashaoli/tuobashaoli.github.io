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
