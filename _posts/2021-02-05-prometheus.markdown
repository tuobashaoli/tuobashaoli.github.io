---
categories: blog
date: '2021-02-05  16:44:18'
description: prometheus
layout: post
published: False
title: "pro me theus"
---

# 简述

Go语言开发

# 架构

- Prometheus Server
	- 抓取：通过服务发现周期抓取job、exporter、pushgateway这三个组件中通过http轮询拉取数据
	- 存储： 通过一定的规则清理和整理数据
		- 本地磁盘
		- 远程存储
	- 查询：通过PromQL查询
- Pushgateway
	- 实现推送模式
	- 临时作业、短作业
	- 批处理作业
	- 应用程序和Prometheus之间有网络隔离
	- 没有UP监控指标和指标过期时进行实例状态监控
- job/exporter
	- 属于prometheus target，是监控的对象
- ServiceDiscovery
	- 支持文件的服务发现，与自动化管理工具Ansible等结合使用
- Alertmanager
	- 单独安装部署，可部署成集群
- Dashboard
	- 实际使用中结合Grafana作为前端界面

适合多个小目标

局限
- 不适合存储事件或者日志
- 默认值存储短期数据
- 集群有问题


# 部署

# PromQL
