# ttsx

#### 项目介绍
一个基于django框架的项目，该项目主要有注册、登录、主页显示、收获地址设置、商品全文检索、加入购物车、提交订单、支付等模块，部分模块由于一些问题
没有上传成功。

#### 软件架构
python3.5 + django1.8.2 + mysql + celery + smtp + haystack + ajax + cookie + session...

#### 安装教程

1. 新建一个虚拟环境（确保是python3.5以上），名字任取，进入到虚拟环境下
2. 在虚拟环境中运行pip install requirements.txt来安装需要的库

#### 使用说明

1. 前期如果需要调试可以将settings.py中DEBUG改为True，ALLOWED_HOSTS设置为空，进入到项目目录下运行python manage.py runserver，
便可以在localhost:8000下运行项目。
2. 后期用了uwsgi加上nginx配置项目上线，所以可以通过运行脚本在后台开启uwsgi和nginx来自动让项目上线，此时ALLOWED_HOST设置为运行
所有pc都可以访问。
3. uwsgi运行方式：uwsgi --ini uwsgi.ini; nginx运行方式：sudo sbin/nginx



