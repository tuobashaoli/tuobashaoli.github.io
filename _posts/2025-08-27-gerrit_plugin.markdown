---
categories: blog
date: '2025-08-27 21:29:18'
description: gerrit插件开发
layout: post
published: True
title: "gerrit插件开发"
tags: gerrit
---

# 下载gerrit源码

建议从github网站上下载，当然从官网上下载也是可以的

`git clone git@github.com:GerritCodeReview/gerrit.git`

# 准备环境

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