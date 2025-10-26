---
categories: blog
date: '2025-10-26 13:08:18'
description: 一些关于项目中多仓库管理技术点的思考
layout: post
published: False
title: "多仓库管理"
tags: devops
---


# 说点儿啥

当项目过于庞大的时候，往往趋向于使用将整个代码分散到多个仓库进行管理，各个仓库对应于项目的哥哥模块，彼此间可以用接口相互关联，但是又可以独立管理，十分地方便

但是怎么管理起来，就一点点说法了

# repo工具

这个是google用来管理Android项目的工具，通过一个文件manifest.xml，里面列出相关的仓库和分支以及各个仓库对应的下载位置，来管理全部的仓库

一个典型的manifest.xml内容如下

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
<remote name="origin" fetch=".." review="review.source.android.com" />
<default revision="master" remote="origin" />
<project name="project/build" path="build">
<copyfile src="makefile" dest="makefile.mk" />
</project>
<project name="project/test" path="test" />
<project name="project/apps/hello" path="apps/hello"/>
</manifest>
```

## 场景1

开发中需要适配各种版本，从而需要生成各种manifest.xml，每个manifest.xml中存储这个版本的各个仓库的分支/哈希节点的信息

比如对应release分支，如下，对应的是v1版本

```
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
<remote name="origin" fetch=".." review="review.source.android.com" />
<default revision="master" remote="origin" />
<!-- project/build是一个通用的仓库，默认分支可以兼容各种发布版本 -->
<project name="project/build" path="build">
<copyfile src="makefile" dest="makefile.mk" />
</project>
<project name="project/test" branch="release_v1" path="test" />
<project name="project/apps/hello" branch="release_v1" path="apps/hello"/>
</manifest>
```

