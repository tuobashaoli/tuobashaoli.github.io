---
categories: blog
date: '2020-05-13 13:04:18'
title: "Javascript"
published: True
layout: post
---

## 基本概念

#### ECMAScript

#### DOM

#### BOM

#### script

defer

async

#### 变量

```javascript
var message = "hi"; //局部变量
obj = "hello"; //全局变量
```

严格模式下，不能定义eval和arguments的变量

#### 数据类型

Undefined、Null、Boolean、Number、String、Object

##### typeof操作符

##### Undefined

undefined，在var声明却没有赋值的时候，变量的值就是undefined

##### Null

只有一个null，undefined派生自null，
```
alert(null == undefined) //true
```

##### Boolean: 

true false

##### Number: 

八进制用0开头，十六进制用0x开头，最小值Number.MIN\_VALUE，最大值Number.MAX\_VALUE；NaN，非数值
```
alert(NaN == NaN) // false
isNaN(NaN) //判断NaN能不能转换成数值，很明显不能，于是返回false，当参数是对象的时候，会先调用valueof方法，如果不行，就调用toString方法
```

Number()、paraseInt()、parseFloat()

##### String

##### Object

```
var o = new Object();
o.hasOwnProperty("name");
o.isPrototypeOf(object);
o.propertyIsEnumerable(proeprtyName);
o.toString();
o.toLocaleString();
o.valueOf();
```

##### 操作符


