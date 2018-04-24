# jdSpider
## 工程说明
本工程主要是获取京东有关于同仁堂的相关产品构建的爬虫程序。工程主要分成三个模块。
1. 单个产品详情获取模块
2. 自动化产品链接抓取模块
3. 保存数据模块(json,es数据库）

## 版本说明
现阶段为v1.0版本.

现阶段已经完成在工程说明中的三个模块的基本构建，下面准备修正详情获取模块中对于中差评的获取的循环控制。

**（现阶段循环控制如果小于一页三十个的评论会出现抓取错误。）**

配合kibana同事进行数据格式的修正

##模块分解
### 详情抓取模块
模块主要实现对于给定的链接商品进行有关于价格、商品名、商品id、评价数、好评数、好评率、中评数、中评率、差评数、差评率、评论详情（评论者id、内容、时间）等内容的获取。

下面为其中一条数据的展示：

{"key": "d", "goods_id": "1168223", "shop_name": "京东自营同仁堂官方旗舰店", "goods_name": "同仁堂破壁灵芝孢子粉胶囊0.35g*90粒", "CommentCount": 34045, "GoodCount": 33601, "GoodRate": 0.988, "GeneralCount": 289, "GeneralRate": 0.008, "PoorCount": 155, "PoorRate": 0.004, "DefaultGoodCount": 10847, "price": "869.00"}

### 自动化获取链接模块
自动化获取链接模块是从搜索页进行产品的id抓取，因为京东方面的产品链接很规则，只需要提供商品id就可以构建商品的链接供详情抓取模块进行使用

下面为其中一条数据的展示：

{"key": "i", "goods_id": "1168223"}

### 数据保存模块
数据保存模块分成两块
1. json文件的保存

为scrapy框架中自带的pipelines功能实现。模块主要是针对数据中的key值的不同进行不同的文件位置的存储，文件分为goods-id、goods-detail、good-{id}-detail三方面的json文件存储。

2. es数据库的写入

## 安装部署

工程需要anaconda的python环境进行运行，在anaconda中需要安装scrapy模块和elasticsearch-dsl模块

需要使用anaconda启动程序，首先启动startGetUrl.py获取产品url，然后运行startSpiders.py对已经抓取的url进行详情抓取

## 依赖关系与配置文件
依赖

- Anaconda3-5.0.1-Linux-x86_64

- Anaconda  - scrapy模块

- Anaconda  - elasticsearch-dsl模块

- elasticsearch6.1.3

- kibana 6.1.3

配置文件需要配置好kibana和es数据库

## 启动方式说明

需要使用anaconda启动程序，首先启动startGetUrl.py获取产品url，然后运行startSpiders.py对已经抓取的url进行详情抓取

在此步之前需要安装好所有依赖软件和各自的模块

1. python startGetUrl.py
2. python startSpiders.py