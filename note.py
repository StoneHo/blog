初始化
    所有Flask 程序都必须创建一个程序实例。Web 服务器使用一种名为Web 服务器网关接口
（Web Server Gateway Interface，WSGI）的协议，把接收自客户端的所有请求都转交给这
个对象处理。程序实例是Flask 类的对象，经常使用下述代码创建：

from flask import Flask
app = Flask(__name__)

    Flask 类的构造函数只有一个必须指定的参数，即程序主模块或包的名字。在大多数程序
中，Python 的__name__ 变量就是所需的值。
    将构造函数的name 参数传给Flask 程序，这一点可能会让Flask 开发新手心
生迷惑。Flask 用这个参数决定程序的根目录，以便稍后能够找到相对于程
序根目录的资源文件位置。




路由
    客户端（例如Web 浏览器）把请求发送给Web 服务器，Web 服务器再把请求发送给Flask
程序实例。程序实例需要知道对每个URL 请求运行哪些代码，所以保存了一个URL 到
Python 函数的映射关系。处理URL 和函数之间关系的程序称为路由。

    在Flask 程序中定义路由的最简便方式，是使用程序实例提供的app.route 修饰器，把修
饰的函数注册为路由。下面的例子说明了如何使用这个修饰器声明路由：

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

修饰器是Python 语言的标准特性，可以使用不同的方式修改函数的行为。惯
常用法是使用修饰器把函数注册为事件的处理程序。




视图函数（view function）
    前例把index() 函数注册为程序根地址的处理程序。如果部署程序的服务器域名为www.
example.com，在浏览器中访问http://www.example.com 后，会触发服务器执行index() 函
数。这个函数的返回值称为响应，是客户端接收到的内容。如果客户端是Web 浏览器，响
应就是显示给用户查看的文档。
    像index() 这样的函数称为视图函数（view function）。视图函数返回的响应可以是包含
HTML 的简单字符串，也可以是复杂的表单。




Context(上下文) 
    context就是对一堆乱七八糟的环境变量的一个听起来好听一点的名字    
    每一段程序都有很多外部变量。只有像Add这种简单的函数才是没有外部变量的。一旦你的一段程序有了外部变量，这
段程序就不完整，不能独立运行。你为了使他们运行，就要给所有的外部变量一个一个写一些值进去。这些值的集合就叫上下文。

Flask上下文全局变量
变量名        上下文                说　　明
current_app   程序上下文   当前激活程序的程序实例
g             程序上下文   处理请求时用作临时存储的对象。每次请求都会重设这个变量
request       请求上下文   请求对象，封装了客户端发出的HTTP 请求中的内容
session       请求上下文   用户会话，用于存储请求之间需要“记住”的值的词典

Flask 在分发请求之前激活（或推送）程序和请求上下文，请求处理完成后再将其删除。程
序上下文被推送后，就可以在线程中使用current_app 和g 变量。类似地，请求上下文被
推送后，就可以使用request 和session 变量。如果使用这些变量时我们没有激活程序上
下文或请求上下文，就会导致错误。
>>> from hello import app
>>> from flask import current_app
>>> current_app.name
Traceback (most recent call last):
...
RuntimeError: working outside of application context
>>> app_ctx = app.app_context()
>>> app_ctx.push()
>>> current_app.name
'hello'
>>> app_ctx.pop()
在这个例子中，没激活程序上下文之前就调用current_app.name 会导致错误，但推送完上
下文之后就可以调用了。注意，在程序实例上调用app.app_context() 可获得一个程序上
下文。




请求钩子
    有时在处理请求之前或之后执行代码会很有用。例如，在请求开始时，我们可能需要创
建数据库连接或者认证发起请求的用户。为了避免在每个视图函数中都使用重复的代码，
Flask 提供了注册通用函数的功能，注册的函数可在请求被分发到视图函数之前或之后
调用。
请求钩子使用修饰器实现。Flask 支持以下4 种钩子。
• before_first_request：注册一个函数，在处理第一个请求之前运行。
• before_request：注册一个函数，在每次请求之前运行。
• after_request：注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
• teardown_request：注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。
在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量g。例如，before_
request 处理程序可以从数据库中加载已登录用户，并将其保存到g.user 中。随后调用视
图函数时，视图函数再使用g.user 获取用户。




响应 返回状态码
    HTTP 响应中一个很重要的部分是状态码，Flask 默认设为200，这个代码表明请求已经被成功处理。
    如果视图函数返回的响应需要使用不同的状态码，那么可以把数字代码作为第二个返回
值，添加到响应文本之后。例如，下述视图函数返回一个400 状态码，表示请求无效：
@app.route('/')
def index():
    return '<h1>Bad Request</h1>', 400



响应 返回Response对象
    make_response() 函数可接受1 个、2 个或3 个参数（和视图函数的返回值一样），并
返回一个Response 对象。有时我们需要在视图函数中进行这种转换，然后在响应对象上调
用各种方法，进一步设置响应。下例创建了一个响应对象，然后设置了cookie：
from flask import make_response
@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response



响应 返回重定向
    重定向经常使用302 状态码表示，指向的地址由Location 首部提供。重定向响应可以使用
3 个值形式的返回值生成，也可在Response 对象中设定。不过，由于使用频繁，Flask 提
供了redirect() 辅助函数，用于生成这种响应：
from flask import redirect
@app.route('/')
def index():
    return redirect('http://www.example.com')



Flask-Script 支持命令行选项
    Flask-Script 是一个Flask 扩展，为Flask 程序添加了一个命令行解析器。Flask-Script 自带
了一组常用选项，而且还支持自定义命令。
示例2-3 显示了把命令行解析功能添加到hello.py 程序中时需要修改的地方。
示例2-3　hello.py：使用Flask-Script
from flask.ext.script import Manager
manager = Manager(app)
# ...
if __name__ == '__main__':
    manager.run()
  专为Flask 开发的扩展都包含在flask.ext 命名空间下。Flask-Script 输出了一个名为
Manager 的类，可从flask.ext.script 中引入。
这样修改之后，程序可以使用一组基本命令行选项。现在运行hello.py，会显示一个用法
消息：
$ python hello.py
usage: hello.py [-h] {shell,runserver} ...
positional arguments:
{shell,runserver}
shell 在Flask 应用上下文中运行Python shell
runserver 运行Flask 开发服务器：app.run()
optional arguments:
-h, --help 显示帮助信息并退出

  shell 命令用于在程序的上下文中启动Python shell 会话。你可以使用这个会话中运行维护
任务或测试，还可调试异常。
  顾名思义，runserver 命令用来启动Web 服务器。运行python hello.py runserver 将以调
试模式启动Web 服务器，但是我们还有很多选项可用：
(venv) $ python hello.py runserver --help
usage: hello.py runserver [-h] [-t HOST] [-p PORT] [--threaded]
[--processes PROCESSES] [--passthrough-errors] [-d]
[-r]
运行Flask 开发服务器：app.run()
optional arguments:
-h, --help 显示帮助信息并退出
-t HOST, --host HOST
-p PORT, --port PORT
--threaded
--processes PROCESSES
--passthrough-errors
-d, --no-debug
-r, --no-reload
--host 参数是个很有用的选项，它告诉Web 服务器在哪个网络接口上监听来自客户端的
连接。默认情况下，Flask 开发Web 服务器监听localhost 上的连接，所以只接受来自服
务器所在计算机发起的连接。下述命令让Web 服务器监听公共网络接口上的连接，允许同
网中的其他计算机连接服务器：
(venv) $ python hello.py runserver --host 0.0.0.0
* Running on http://0.0.0.0:5000/
* Restarting with reloader
现在，Web 服务器可使用http://a.b.c.d:5000/ 网络中的任一台电脑进行访问，其中“a.b.c.d”
是服务器所在计算机的外网IP 地址。



render_template 渲染模板
示例3-3　hello.py：渲染模板
from flask import Flask, render_template
# ...
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

  Flask 提供的render_template 函数把Jinja2 模板引擎集成到了程序中。render_template 函
数的第一个参数是模板的文件名。随后的参数都是键值对，表示模板中变量对应的真实
值。在这段代码中，第二个模板收到一个名为name 的变量。
  前例中的name=name 是关键字参数，这类关键字参数很常见，但如果你不熟悉它们的话，
可能会觉得迷惑且难以理解。左边的“name”表示参数名，就是模板中使用的占位符；右
边的“name”是当前作用域中的变量，表示同名参数的值。



关键字参数
    可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。
而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。
请看示例：

def person(name, age, **kw):
    print 'name:', name, 'age:', age, 'other:', kw
函数person除了必选参数name和age外，还接受关键字参数kw。在调用该函数时，可以只传入必选参数：

>>> person('Michael', 30)
name: Michael age: 30 other: {}
也可以传入任意个数的关键字参数：

>>> person('Bob', 35, city='Beijing')
name: Bob age: 35 other: {'city': 'Beijing'}
>>> person('Adam', 45, gender='M', job='Engineer')
name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
  关键字参数有什么用？它可以扩展函数的功能。比如，在person函数里，我们保证能接收到name和age这两个参数，
但是，如果调用者愿意提供更多的参数，我们也能收到。试想你正在做一个用户注册的功能，除了用户名和年龄是必填项外，其他都是可选项，利用关键字参数来定义这个函数就能满足注册的需求。

和可变参数类似，也可以先组装出一个dict，然后，把该dict转换为关键字参数传进去：

>>> kw = {'city': 'Beijing', 'job': 'Engineer'}
>>> person('Jack', 24, city=kw['city'], job=kw['job'])
name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}
当然，上面复杂的调用可以用简化的写法：

>>> kw = {'city': 'Beijing', 'job': 'Engineer'}
>>> person('Jack', 24, **kw)
name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}




Jinja2变量过滤器
示例3-2　 templates/user.html：Jinja2 模板
<h1>Hello, {{ name }}!</h1>
  示例3-2 在模板中使用的{{ name }} 结构表示一个变量，它是一种特殊的占位符，告诉模
板引擎这个位置的值从渲染模板时使用的数据中获取。
  可以使用过滤器修改变量，过滤器名添加在变量名之后，中间使用竖线分隔。例如，下述
模板以首字母大写形式显示变量name 的值：
Hello, {{ name|capitalize }}
表3-1 列出了Jinja2 提供的部分常用过滤器。
表3-1　Jinja2变量过滤器
过滤器名         说　　明
safe          渲染值时不转义
capitalize    把值的首字母转换成大写，其他字母转换成小写
lower         把值转换成小写形式
upper         把值转换成大写形式
title         把值中每个单词的首字母都转换成大写
trim          把值的首尾空格去掉
striptags     渲染之前把值中所有的HTML 标签都删掉



控制结构
  Jinja2 提供了多种控制结构，可用来改变模板的渲染流程。本节使用简单的例子介绍其中
最有用的控制结构。

下面这个例子展示了如何在模板中使用条件控制语句：

{% if user %}
    Hello, {{ user }}!
{% else %}
    Hello, Stranger!
{% endif %}

另一种常见需求是在模板中渲染一组元素。下例展示了如何使用for 循环实现这一需求：

<ul>
    {% for comment in comments %}
        <li>{{ comment }}</li>
    {% endfor %}
</ul>

Jinja2 还支持宏。宏类似于Python 代码中的函数。例如：

{% macro render_comment(comment) %}
    <li>{{ comment }}</li>
{% endmacro %}

<ul>
    {% for comment in comments %}
        {{ render_comment(comment) }}
    {% endfor %}
</ul>

为了重复使用宏，我们可以将其保存在单独的文件中，然后在需要使用的模板中导入：

{% import 'macros.html' as macros %}
<ul>
    {% for comment in comments %}
        {{ macros.render_comment(comment) }}
    {% endfor %}
</ul>
`
需要在多处重复使用的模板代码片段可以写入单独的文件，再包含在所有模板中，以避免
重复：
{% include 'common.html' %}
另一种重复使用代码的强大方式是模板继承，它类似于Python 代码中的类继承。首先，创
建一个名为base.html 的基模板:

<html>
<head>
    {% block head %}
    <title>{% block title %}{% endblock %} - My Application</title>
    {% endblock %}
</head>
<body>
    {% block body %}
    {% endblock %}
</body>
</html>

block 标签定义的元素可在衍生模板中修改。在本例中，我们定义了名为head、title 和
body 的块。注意，title 包含在head 中。下面这个示例是基模板的衍生模板：

{% extends "base.html" %}
{% block title %}Index{% endblock %}
{% block head %}
    {{ super() }}
    <style>
    </style>
{% endblock %}
{% block body %}
<h1>Hello, World!</h1>
{% endblock %}

extends 指令声明这个模板衍生自base.html。在extends 指令之后，基模板中的3 个块被
重新定义，模板引擎会将其插入适当的位置。注意新定义的head 块，在基模板中其内容不
是空的，所以使用super() 获取原来的内容。



@classmethod & @staticmethod

类中最常用的方法是实例方法, 即通过通过实例作为第一个参数的方法。
举个例子，一个基本的实例方法就向下面这个:

 
class Kls(object):
    def __init__(self, data):
        self.data = data
    def printd(self):
        print(self.data)
ik1 = Kls('arun')
ik2 = Kls('seema')
ik1.printd()
ik2.printd()

这会给出如下的输出:
arun
seema



然后看一下代码和示例图片:
1，2参数传递给方法.
3 self参数指向当前实例自身.
4 我们不需要传递实例自身给方法，Python解释器自己会做这些操作的.
如果现在我们想写一些仅仅与类交互而不是和实例交互的方法会怎么样呢? 
我们可以在类外面写一个简单的方法来做这些，
但是这样做就扩散了类代码的关系到类定义的外面. 
如果像下面这样写就会导致以后代码维护的困难:

 
def get_no_of_instances(cls_obj):
    return cls_obj.no_inst
class Kls(object):
    no_inst = 0
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
ik1 = Kls()
ik2 = Kls()
print(get_no_of_instances(Kls))

输出:
2
@classmethod
我们要写一个只在类中运行而不在实例中运行的方法.
 如果我们想让方法不在实例中运行，可以这么做:

 
def iget_no_of_instance(ins_obj):
    return ins_obj.__class__.no_inst
class Kls(object):
    no_inst = 0
    def __init__(self):
    Kls.no_inst = Kls.no_inst + 1
ik1 = Kls()
ik2 = Kls()
print iget_no_of_instance(ik1)

输出
2
在Python2.2以后可以使用@classmethod装饰器来创建类方法.

 
class Kls(object):
    no_inst = 0
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
    @classmethod
    def get_no_of_instance(cls_obj):
        return cls_obj.no_inst
ik1 = Kls()
ik2 = Kls()
print ik1.get_no_of_instance()
print Kls.get_no_of_instance()

输出:
2
2
这样的好处是: 不管这个方式是从实例调用还是从类调用，它都用第一个参数把类传递过来.
@staticmethod
经常有一些跟类有关系的功能但在运行时又不需要实例和类参与的情况下需要用到静态方法. 比如更改环境变量或者修改其他类的属性等能用到静态方法. 这种情况可以直接用函数解决, 但这样同样会扩散类内部的代码，造成维护困难.
比如这样:

 
IND = 'ON'
def checkind():
    return (IND == 'ON')
class Kls(object):
     def __init__(self,data):
        self.data = data
def do_reset(self):
    if checkind():
        print('Reset done for:', self.data)
def set_db(self):
    if checkind():
        self.db = 'new db connection'
        print('DB connection made for:',self.data)
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()

输出:
Reset done for: 12
DB connection made for: 12
如果使用@staticmethod就能把相关的代码放到对应的位置了.
 
IND = 'ON'
class Kls(object):
    def __init__(self, data):
        self.data = data
    @staticmethod
    def checkind():
        return (IND == 'ON')
    def do_reset(self):
        if self.checkind():
            print('Reset done for:', self.data)
    def set_db(self):
        if self.checkind():
            self.db = 'New db connection'
        print('DB connection made for: ', self.data)
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()

输出:
Reset done for: 12
DB connection made for: 12
下面这个更全面的代码和图示来展示这两种方法的不同
@staticmethod 和 @classmethod的不同

 
class Kls(object):
    def __init__(self, data):
        self.data = data
    def printd(self):
        print(self.data)
    @staticmethod
    def smethod(*arg):
        print('Static:', arg)
    @classmethod
    def cmethod(*arg):
        print('Class:', arg)
 
>>> ik = Kls(23)
>>> ik.printd()
23
>>> ik.smethod()
Static: ()
>>> ik.cmethod()
Class: (<class '__main__.Kls'>,)
>>> Kls.printd()
TypeError: unbound method printd() must be called with Kls instance as first argument (got nothing instead)
>>> Kls.smethod()
Static: ()
>>> Kls.cmethod()
Class: (<class '__main__.Kls'>,)




@property
在绑定属性时，如果我们直接把属性暴露出去，虽然写起来很简单，但是，没办法检查参数，导致可以把成绩随便改：

s = Student()
s.score = 9999
这显然不合逻辑。为了限制score的范围，可以通过一个set_score()方法来设置成绩，再通过一个get_score()来获取成绩，这样，在set_score()方法里，就可以检查参数：

class Student(object):

    def get_score(self):
        return self._score

    def set_score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
现在，对任意的Student实例进行操作，就不能随心所欲地设置score了：

>>> s = Student()
>>> s.set_score(60) # ok!
>>> s.get_score()
60
>>> s.set_score(9999)
Traceback (most recent call last):
  ...
ValueError: score must between 0 ~ 100!
但是，上面的调用方法又略显复杂，没有直接用属性这么直接简单。
有没有既能检查参数，又可以用类似属性这样简单的方式来访问类的变量呢？
对于追求完美的Python程序员来说，这是必须要做到的！
还记得装饰器（decorator）可以给函数动态加上功能吗？
对于类的方法，装饰器一样起作用。Python内置的@property装饰器就是负责把一个方法变成属性调用的：

class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
@property的实现比较复杂，我们先考察如何使用。把一个getter方法变成属性，只需要加上@property就可以了，此时，@property本身又创建了另一个装饰器@score.setter，负责把一个setter方法变成属性赋值，于是，我们就拥有一个可控的属性操作：

>>> s = Student()
>>> s.score = 60 # OK，实际转化为s.set_score(60)
>>> s.score # OK，实际转化为s.get_score()
60
>>> s.score = 9999
Traceback (most recent call last):
  ...
ValueError: score must between 0 ~ 100!
注意到这个神奇的@property，我们在对实例属性操作的时候，就知道该属性很可能不是直接暴露的，而是通过getter和setter方法来实现的。

还可以定义只读属性，只定义getter方法，不定义setter方法就是一个只读属性
class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2014 - self._birth
上面的birth是可读写属性，而age就是一个只读属性，因为age可以根据birth和当前时间计算出来。




@login_required
示例8-21　app/auth/views.py：确认用户的账户
from flask.ext.login import current_user
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
if current_user.confirmed:
return redirect(url_for('main.index'))
if current_user.confirm(token):
flash('You have confirmed your account. Thanks!')
else:
flash('The confirmation link is invalid or has expired.')
return redirect(url_for('main.index'))
Flask-Login 提供的login_required 修饰器会保护这个路由，因此，用户点击确认邮件中的
链接后，要先登录，然后才能执行这个视图函数。
这个函数先检查已登录的用户是否已经确认过，如果确认过，则重定向到首页，因为很
显然此时不用做什么操作。这样处理可以避免用户不小心多次点击确认令牌带来的额外
工作。




current_user
  示例8-10　app/templates/base.html：导航条中的Sign In 和Sign Out 链接
<ul class="nav navbar-nav navbar-right">
{% if current_user.is_authenticated() %}
<li><a href="{{ url_for('auth.logout') }}">Sign Out</a></li>
{% else %}
<li><a href="{{ url_for('auth.login') }}">Sign In</a></li>
{% endif %}
</ul>
判断条件中的变量current_user 由Flask-Login 定义，且在视图函数和模板中自动可用。
这个变量的值是当前登录的用户，如果用户尚未登录，则是一个匿名用户代理对象。如果
是匿名用户，is_authenticated() 方法返回False。所以这个方法可用来判断当前用户是否
已经登录。




