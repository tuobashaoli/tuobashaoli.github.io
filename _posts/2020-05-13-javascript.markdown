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

#### 操作符

##### 位操作符

```javascript
~、&、|、^、有符号右移>>、无符号右移>>>
```

##### 相等操作符

```javascript
"5" == 5 // true
Nan == NaN // false
null == undeined // true
undefined == 0 //false
null == 0 //false

"55" === 55 //false 因为转换了对比对象才相等，所以不等
"55" !== 55 //true 因为不转换就不相同了，实际是因为类型不同，也就是类型和数值都要一样
```

#### with

```
with(location) {
    var qs = search.substring(1)
}
```

#### switch

比较的时候使用的是全等操作符

#### 函数

##### 参数

很松散，定义的参数不一定在调用时传参，也可以在函数内使用argument(这个类似数组)访问传入的参数，

#### 作用域

没有块级作用域

```javascript
if(true){
var color="blue";
}
alert(color) //"blue"
```

var定义的变量会绑定到当前的环境，如果没有用var定义，则会将变量变成全局变量

#### object类型

```javascript
var obj = new object();
var person = {
    "name":"gsl",
    "age":24
};

person["name"] //gsl
person.name //gsl
```
#### Array

```javascript
var colors = new Array();
var colors2 = new Array(20);
var colors3 = new Array("blue","green");
var colors4 = ["red","blue","green"];

colors.length = 2 // 不是只读的，可以修改的

Array.isArray(value) //支持的浏览器怪多的

colors2.toLocaleString() // 调用的是数组里面的每个元素的toLocaleString()方法获取返回值

colors3.join("|") // red|blue|green

colors3.push("black") //["red","blue","green","black"]

colors3.pop()

colors3.shift()

colors3.unshift("grey")

colors3.reverse();

colors3.sort(compare);

colors3.concat("yellow",["f","orange"]) // ["red","blue","green","black","yellow","f","orange"]

colors3.slice(1,3) //返回第1、2、3个元素

colors3.splice(1,2,"brown") // 从位置1开始删除2个元素，然后加入一个"brown"

colors3.indexof("yellow")

colors3.lastindexof("red")
```

#### Date

```javascript
var now = new Date();
```

#### RegExp

```javascript
var expression = /pattern/flag ;

/*
* flag:
*    g 全局匹配
*    i 不区分大小写
*    m 多行模式
*/

var pattern  = /[bc]at/i;

var pattern2 = new RegExp("[bc]at","i");

var matches = pattern2.exec("cat bat a cat");

pattern.test("cat") //返回true或者false
```

#### Function

##### 内部属性

###### arguments

arguments.callee,指向拥有这个arguments对象的函数

###### this

在全局环境中调用函数时，函数中的this就是window

###### caller属性

显示函数的调用者，严格模式下不能使用
###### length属性

函数期望接收的参数的个数

###### prototype属性

##### 基本包装类型

对基本类型的包装，自动创建的基本包装类型的对象，只存在于一行代码执行瞬间。

```javascript
var s1 = "some";
s1.jkl = "rookie";
alert(s1.jkl) // undefined

var num = Number(1);
alert(typeof num); // number
var num = new Number(2);
alert(typeof num);// object
```

###### Boolean

建议不要用，因为基本包装类型在需要真值时都会被转成true

###### Number

```javascript
var num = 10;
alert(num.toString(8)); // "12"

alert(num.toFixed(2)); // "10.00"

alert(num.toExponential(1)) //"1.0e+1" 科学计数法

var num = 99;

alert(num.toPercision(1)); //
```

###### String

```javascript
var ss = "string code";
ss.charAt(1);
ss.charCodeAt(1);//116
ss[2];
ss.concat(" hello");//返回"string code hello"，不改变ss
ss.slice(3,7); //"ing "
ss.substr(3,3); //"ing"
ss.substring(3,7); //"ing "

var bb = "hello world";
bb.indexof("o");//4
bb.lastIndexOf("o");//7
bb.indexof("o",6);//7,从位置6开始向后搜索
bb.lastIndexOf("o",4);//4，从位置4向前搜索

var uu = " hello ";
var uc = uu.trim();

var yy = "jkl";
var rookie = yy.toLocaleUpperCase();
var shy = yy.toUpperCase();
var ning = yy.toLocaleLowerCase();
var baolan = yy.toLowerCase();

var pattern = /.at/;
var text = "cat,bat,";
var matches = text.match(pattern);
var pos = text.search(/at/);

var result = text.replace("at","cond"); // "cond,bat,"
var result = text.replace(/at/g,"cond"); // "cond,bond," 

var result = text.split(",",1);// ["cat"]

var result = text.localeCompare("hehe");//1,大多数是这样的
```

##### Global对象

```javascript
var uri = "http://www.baidu.com/hello world";

encodeURI(uri); //"http://www.baidu.com/hello%20world"
encodeURIComponent(uri);//"http%3A%2F%2Fwww.badu.com%2Fhello%20world"

eval("alert('hi')");//看起来像是创造了一个子进程，在子进程里面执行javascript语句，严格模式下主进程无法获取eval中定义的对象，当然只是这么理解。

window.innerWidth //1920
```
##### Math对象

## 面向对象

### 创建对象

#### 工厂模式

```javascript

```

#### 构造函数模式

```javascript

```

#### 原型

```javascript
function Person(){
}

Person.prototype.name = "Tony";
Person.prototype.sayName = function(){
    alert(this.name);
};

var person1 = new Person();
person1.sayName();
```
