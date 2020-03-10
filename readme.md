# Bartender Chatbot
这是一个简单的聊天机器人，你可以通过它获取关于鸡尾酒的知识。基于wxpy模块，实现了在微信界面的聊天。
***
# 演示GIF
- 这是用查询酒Daiquiri相关信息作为实例：

![](https://github.com/bbduo/bartender_chatbot/blob/master/img/windows.gif)

- 这是用查询Margarita酒相关信息作为实例：

![](https://github.com/bbduo/bartender_chatbot/blob/master/img/iphone.gif)

***

# 用来干啥
- 本程序面向鸡尾酒爱好者，你可以通过它来获取鸡尾酒相关资料。具有以下几个功能：

1. 查询鸡尾酒的评价
2. 查询鸡尾酒的酒杯
3. 查询鸡尾酒图片
4. 教你调酒(调酒方法)
5. 查询调酒的材料
6. 推荐一款酒
***

# 实现技术
1.本程序基于 **RASA NLU** (Version: 0.15.1)版本及其支持的外部组件实现的。RASA的训练数据通过[rasa-nlu-trainer](https://rasahq.github.io/rasa-nlu-trainer/)训练得到json文件。rasa的配置文件如下：

	```
	language: "en_core_web_md"

	pipeline:”spacy_sklearn”
	```

2.本程序通过 https://www.thecocktaildb.com/api.php 的 api 接口实现鸡尾酒数据库的调用。

方法| 描述 |
 :-: | :--: |
查询酒的相关信息|[search](https://www.thecocktaildb.com/api/json/v1/1/search.php?)|
查询酒的信息(id)|[lookup](https://www.thecocktaildb.com/api/json/v1/1/lookup.php?)|
通过种类过滤不同酒 |[filter](https://the-cocktail-db.p.rapidapi.com/filter.php?)|

3.通过 **wxpy** (Version: 0.3.9.8)将本程序在微信上面得以实现做成界面。

***

# 代码说明

- 函数说明

函数| 作用
 :-: | :-: | :-:
search_instruction(drinks) | 找到一款酒的调酒方法 |
search_drink_inform(drinks)|找到一款酒的信息（酒杯，照片，评价）|
search_materials(drinks)|找到一款酒的调酒配料|
search_cate_drink(cate)|找到某一类鸡尾酒里的一种|
send_message(policy, state, message)|发送消息|
respond(policy, state, message)|得到回复|
find_cocktails(message)|找到鸡尾酒名|

- 流程图：
以实现功能查询鸡尾酒信息为例：


![](https://github.com/bbduo/bartender_chatbot/blob/master/img/3.png)
***
# 配置环境
1.	git clone代码
2.	我的python版本是3.7.0
3.	安装必要的包
	```
	pip install requests  # 获取api数据时要用(我的版本:	2.23.0)

	# 从豆瓣 PYPI 镜像源下载安装 (推荐国内用户选用)(我的版本:	0.3.9.8)
	pip install -U wxpy -i "https://pypi.doubanio.com/simple/" # 集成到微信界面时用


	pip install rasa # 处理消息得到半结构化语句用到(我的版本: 0.15.1)
	```


***
# 开始使用bot

1.	训练模型
 - 通过上述所给的RASA **配置文件**和**训练数据**来训练模型，命令行代码如下：

```
python -m rasa_nlu.train -c config_spacy.yml --data demo-rasa-onlyintent.json --project nlu
```

- 你也可以通过models/nlu/nlu目录下直接获取我训练的模型。(效果有针对性)
  
2.	调用数据库
- 通过上述API链接，和requests模块获取数据,seach开头的函数已经实现了这一点。
3.	如果只需要在命令行和Bartender聊天，则**只需要**运行main.py
4.	如果需要在微信界面和Bartender聊天，则**只需要**运行main_wechat.py
- 说明：程序运行后，会弹出二维码，扫描二维码后显示登陆成功。
	```
	# 导入模块
	from wxpy import *
	# 初始化机器人，扫码登陆
	bot = Bot()
	```
请开始愉快的聊天吧
***
# 参考网站
- [rasa使用和训练](https://blog.csdn.net/m0epNwstYk4/article/details/80479967)  RASA NLU 抽取实体和识别意图很详尽
- [rasa官方文档](https://rasa.com/docs/rasa/nlu/about/)
- [个人搭建chatbot](https://blog.csdn.net/qq_39241986/article/details/82050472) 对wxpy能有一个从头到尾的介绍
- [wxpy官方参考](https://github.com/youfou/wxpy)

***
# 程序局限性

- 实现功能比较单调
- 意图识别效果较为基础，有待丰富训练数据，增强模型



#### (还是第一版，正在优化更新中！！！)
