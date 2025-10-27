---
categories: blog
date: '2025-10-26 13:08:18'
description: 一些关于项目中多仓库管理技术点的思考
layout: post
published: True
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

这里的project没有指定分支branch或者revision，就表示默认下载默认分支master上最新的节点的代码

## 场景1

获取主线master版本的最新代码，通常用于持续集成和定时构建，如下

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

使用各个仓库的主线分支，每次下载都是下载这些仓库的主线分支master上的最新代码

## 场景2

开发中需要适配各种版本，从而需要生成各种manifest.xml，每个manifest.xml中存储这个版本的各个仓库的分支/哈希节点的信息

比如对应release分支，如下，对应的是v1版本

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
<remote name="origin" fetch=".." review="review.source.android.com" />
<default revision="master" remote="origin" />
<!-- project/build是一个通用的仓库，默认分支可以兼容各种发布版本 -->
<project name="project/build" path="build">
<copyfile src="makefile" dest="makefile.mk" />
</project>
<project name="project/test" revision="release_v1" path="test" />
<project name="project/apps/hello" revision="release_v1" path="apps/hello"/>
</manifest>
```

## 场景3

某个节点的全部代码都已经测试完毕，bug收敛，达到发布质量标准了，并对每个仓库创建了标记号TAG，比如V1.0

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
<remote name="origin" fetch=".." review="review.source.android.com" />
<default revision="master" remote="origin" />
<!-- project/build是一个通用的仓库，默认分支可以兼容各种发布版本 -->
<project name="project/build" revision="V1.0" path="build">
<copyfile src="makefile" dest="makefile.mk" />
</project>
<project name="project/test" revision="V1.0" path="test" />
<project name="project/apps/hello" revision="V1.0" path="apps/hello"/>
</manifest>
```

这样在任意时刻，使用这个manifest下载的代码，都是固定的

## 场景4

当一个大项目中，不同团队开发不同的仓库，但是也存在公共仓库供多个团队开发,如下所示，


```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
<remote name="origin" fetch=".." review="review.source.android.com" />
<default revision="master" remote="origin" />
<!-- project/build是一个通用的仓库，默认分支可以兼容各种发布版本 -->
<project name="project/build" groups="public" path="build">
<copyfile src="makefile" dest="makefile.mk" />
</project>
<project name="project/test" groups="public" path="test" />
<project name="project/apps/hello" groups="hello" path="apps/hello"/>
<project name="project/apps/world" groups="world" path="apps/world"/>
</manifest>
```

hello团队和world团队分别负责自己的仓库，但是project/build和project/test是公共仓库

hello团队使用这个manifest下载时使用命令`repo init -u <manifest_url> -b <branch> -g public,hello`

world团队使用这个manifest下载时使用命令`repo init -u <manifest_url> -b <branch> -g public,world`

## 场景5

当仓库不全部都是来源于一个代码源，如下所示

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
<remote name="origin" fetch=".." review="review.source.android.com" />
<remote name="origin2" fetch=".." review="review2.source.android.com" />
<default revision="master" remote="origin" />
<!-- project/build是一个通用的仓库，默认分支可以兼容各种发布版本 -->
<project name="project/build" revision="V1.0" path="build" remote="origin2">
<copyfile src="makefile" dest="makefile.mk" />
</project>
<project name="project/test" revision="V1.0" path="test" />
<project name="project/apps/hello" revision="V1.0" path="apps/hello"/>
</manifest>
```

这样，project/build的代码就从review2.source.android.com地址下载，其他仓库就从review.source.android.com下载

## 总结

可见，使用manifest可以非常灵活地管理各个仓库，如果某个仓库有更新，直接更改manifest里面的仓库的revision就可以实现了，

缺点就是需要用户额外学习manifest的使用和配置了，并且manifest也是存放在一个git仓库里面的，所以这个manifest的git仓库也需要额外管理


# git submodule

子模块是内嵌入git的，相关配置都是在git仓库的.gitmodules文件里面，如下所示

```
[submodule "libfoo"]
  path = src/libfoo
  url = https://github.com/example/libfoo.git
  branch = dev

[submodule "utils"]
  path = src/utils
  url = ../utils-repo.git  # 相对路径
  branch = release
```

子模块存储在git里面的只能是hash，所以每次子模块存在更新换了新的hash时，都要在git中下载子模块然后做个提交

好处是不需要用户额外学习安装repo，只需要记住几个常用的git submodule命令即可


## 公共模块更新

当一个公共的仓库有更新时，就需要让所有的包含这个公共仓库的仓库，去进行更新，比较麻烦

比如，hello仓库和world仓库都需要build仓库，那么在hello仓库和world仓库的.gitmodules文件里面都写上如下内容

```
[submodule "build"]
  path = project/build
  url = git@review.source.android.com/project/build
  branch = master
```

当build仓库有更新的时候，就要把hello仓库和world仓库的子模块build都去更新一下hash，

1. repo manifest只需要修改xml文件里面仓库的revision为目标hash
2. git submodule需要下载submodule的代码并且checkout到目标hash然后提交，仓库越大耗时越长


## 模拟repo manifest

假设，有个git仓库叫manifest，里面的.gitmodules内容如下

```
[submodule "build"]
  path = project/build
  url = git@review.source.android.com/project/build
  branch = master
[submodule "test"]
  path = project/test
  url = git@review.source.android.com/project/test
  branch = master
[submodule "hello"]
  path = project/hello
  url = git@review.source.android.com/project/hello
  branch = master
```

这样这个仓库连带submodule下载完，其实代码格局和repo manifest是十分相似的，但是

1.repo manifest中的revision可以直接看出仓库的hash节点，所以在交付源码时，直接发送一个revision是固定hash的xml即可
2.git submodule中的.gitmodules显示仓库的hash节点，必须把仓库下载到对应hash然后才能查看各个submodule的hash，比较麻烦

**个人感觉**这种模拟的效果是不如repo manifest的


## 总结

对于一些简单的仓库依赖场景，比如各个仓库呈现层数不高的树状依赖，就可以使用git submodule来简化操作,如下所示

```
     build
     /  \
hello    world

    test
    /  \
hello   world
```

如果是大型项目，存在上百个仓库，十几个开发团队协作，并且存在仓库之间的相互依赖，比如Android项目，还是推荐使用repo manifest管理
