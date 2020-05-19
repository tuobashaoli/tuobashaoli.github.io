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

```javascript
alert(null == undefined) //true
```

##### Boolean: 

true false

##### Number: 

八进制用0开头，十六进制用0x开头，最小值Number.MIN\_VALUE，最大值Number.MAX\_VALUE；NaN，非数值

```javascript
alert(NaN == NaN) // false
isNaN(NaN) //判断NaN能不能转换成数值，很明显不能，于是返回false，当参数是对象的时候，会先调用valueof方法，如果不行，就调用toString方法
```

Number()、paraseInt()、parseFloat()

##### String

##### Object

```javascript
var o = new Object();
o.hasOwnProperty("name");
o.isPrototypeOf(object);
o.propertyIsEnumerable(proeprtyName);
o.toString();
o.toLocaleString();
o.valueOf();
```

##### 操作符

###### 位操作符

```javascript
~、&、|、^、有符号右移>>、无符号右移>>>
```

###### 相等操作符

```javascript
"5" == 5 // true
Nan == NaN // false
null == undeined // true
undefined == 0 //false
null == 0 //false

"55" === 55 //false 因为转换了对比对象才相等，所以不等
"55" !== 55 //true 因为不转换就不相同了，实际是因为类型不同，也就是类型和数值都要一样
```

##### with

```
with(location) {
    var qs = search.substring(1)
}
```

##### switch

比较的时候使用的是全等操作符

##### 函数

###### 参数

很松散，定义的参数不一定在调用时传参，也可以在函数内使用argument(这个类似数组)访问传入的参数，

##### 作用域

没有块级作用域

```javascript
if(true){
var color="blue";
}
alert(color) //"blue"
```

var定义的变量会绑定到当前的环境，如果没有用var定义，则会将变量变成全局变量

##### object类型

```javascript
var obj = new object();
var person = {
    "name":"gsl",
    "age":24
};

person["name"] //gsl
person.name //gsl
```
##### Array

```javascript
var colors = new Array();
var colors2 = new Array(20);
var colors3 = new Array("blue","green");
var colors4 = ["red","blue","green"];

colors.length = 2 // 不是只读的，可以修改的

Array.isArray(value) //支持的浏览器怪多的

colors2.toLocaleString() // 调用的是数组里面的每个元素的toLocaleString()方法获取返回值
```


