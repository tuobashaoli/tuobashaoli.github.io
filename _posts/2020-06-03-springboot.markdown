---
categories: blog
date: '2020-06-03 15:36:18'
title: "Springboot"
published: True
layout: post
---


### 常用注解

```
@Entity //orm实体，对应数据库表
@Data //提供读写属性
@Table(name="tbl_Identity") //表的名称
public class Identity {

//需要一个Id字段
@Id
@Column(name = "Id")
private String Id;

//一个普通的字段
@Column
private String Description;
}
```

```
@Configuration //@Configuration用于定义配置类，可替换xml配置文件，被注解的类内部包含有一个或多个被@Bean注解的方法，这些方法将会被AnnotationConfigApplicationContext或AnnotationConfigWebApplicationContext类进行扫描，并用于构建bean定义，初始化Spring容器
@Slf4j //定义log
public class DataSourceConfig {
@Bean(name="demoDataSource")
@Primary
@Qualifier("demoDataSource")
@ConfigurationProperies(prefix="spring.datasource")
public Datasource demoDataSource(){
    log.info("---init---");
    return DataSourceBuilder.create().build();
}
}
```
