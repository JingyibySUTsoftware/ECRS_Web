# 基于深度学习的商品推荐系统

### 项目简介
#### 技术栈
>项目用到的技术如下：
语言：`Python3` `Java`
Web端：`Layui`,`Flask`,`Nginx`,`Gevent`，`Flask_Cache`
模型训练： `PaddleRec` , `PaddlePaddle` 
深度学习模型:`DSSM`, `DeepFM`
向量召回：`milvus`
数据存储： `Redis` 
模型推理： `PaddleServing`
模块通信：`gRPC`,`protobuf`

#### 快速开始
##### 项目部署依赖
Python3、PaddlePaddle2.2.2、PaddleServing、milvus1.0、redis、nginx、Gevent

PaddlePaddle安装参考 ：[PaddlePaddle飞桨安装](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/develop/install/pip/windows-pip.html)

Milvus的安装请参考：[Milvus安装](https://blog.csdn.net/weixin_44524687/article/details/125191687?csdn_share_tail=%7B%22type%22:%22blog%22,%22rType%22:%22article%22,%22rId%22:%22125191687%22,%22source%22:%22weixin_44524687%22%7D&ctrtid=w3I8z)

Milvus的python驱动和PaddleServing安装
```shell
python3 -m pip install redis pymilvus==1.0.1 paddle_serving_app==0.3.1
```
gevent模块安装
```shell
pip install gevent
```
Flask_Cache模块安装
```shell
pip install Flask-Cache
```
##### 项目启动
当你安装以上依赖后，保证Redis和Milvus处于运行状态

1.向Redis中存储用户和商品数据
```shell
python to_redis.py
```
2.向Milvus中存储商品向量数据
```shell
python to_milvus.py
```
3.启动用户服务
```shell
python um.py
```
4.启动内容服务
```shell
python cm.py
```
5.启动召回服务
```shell
python recall.py
```
6.启动排序服务
```shell
python rank.py
```
7.启动Web应用
```shell
python controller.py

python controller2.py
```
到这里就可以使用系统了，在浏览器访问 `http://localhost:5000`和`http://localhost:5001`即可体验使用
如果还需要进行负载均衡可以运行Nginx，该项目中的Nginx配置内容请参考[Nginx配置](https://blog.csdn.net/weixin_44524687/article/details/125210575)
如果您配置了Nginx，则在浏览器中访问 `http://loclhost:5158`使用本系统

#### 跨平台功能说明
本项目中内置了一个跨平台演示Demo在`ECRS_jav_demo`文件夹下，直接运行该文件夹下`Client.java`文件，即可体验使用Java访问python编写的推荐服务模块，如果需要定制访问其他服务请参考[跨平台访问](https://blog.csdn.net/weixin_44524687/article/details/124614018)

#### 系统架构及推荐流程
系统架构
![在这里插入图片描述](https://img-blog.csdnimg.cn/873403086dbb4f3795844f7661ffe376.png)
系统工作流程
![在这里插入图片描述](https://img-blog.csdnimg.cn/b449665335644d5a84ed2b2938fceef6.png)
推荐功能流程图
![在这里插入图片描述](https://img-blog.csdnimg.cn/59e7fa6c55ef412cbbbdc71c3ea33f65.png)




(1)登录。
系统的默认起始页，所有用户第一次访问系统时，都将访问该页面，同时该页面还承担着请求流量承载的功能。
(2)用户服务/商品服务。
将实验用的数据集进行拆分，用户数据和商品数据各一份，数据经过解析保存到非关系型数据库 Redis 中，外部传入用户和商品的唯一id 作为 key 到 Redis 中查找对应的 value 并以二进制流的形式将结果返回到相应的模块。
(3)召回服务。
召回服务主要有三个任务，当系统中有新用户使用时，上述的用户信息库中无法查询该用户的信息。系统可以利用原有的用户信息训练的模型拟合新增用户，新用户会通过这个用户模型得到该用户的特征向量；为了完成召回任务，需要提前将所有商品信息通过商品模型转换成商品特征向量并导入 Milvus 中，同理， 当有新商品上架时，需要预执行上述步骤以便新商品可以及时地被推荐；最后把用户向量和商品向量在Milvus 中做向量近似搜索，返回只包含商品id信息的候选集列表。 
(4)排序服务。
召回阶段得到的候选集商品 id 列表通过商品服务查询商品的详细信息，然后与用户向量结合作为排序服务的输入，排序模型通过打分把所有候 选待推荐的商品按分数从高到低排序，最后返回这个含有详细商品信息的推荐列表。
(5)接口服务。
后台每个功能模块通过gRPC框架划分为微服务模块，每个服务拥有独立的通信端口channel，开发者可以根据需要向指定的模块的channel发送请求参数，模块接受到参数处理后返回结果。


![在这里插入图片描述](https://img-blog.csdnimg.cn/eac9c45de18c423b815ebdc65a3e22dc.png)










#### 结果演示示例（仅展示部分功能页面）
您也可以查看系统的演示视频[Bilibili在线演示](https://www.bilibili.com/video/BV1GZ4y1t7bL/)
![在这里插入图片描述](https://img-blog.csdnimg.cn/069fc076288648d1ba9825d65163dbc2.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/59b9e50247234ea48b9d2b192994ca33.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/fcfbc59585f14126b38ec714cac55f45.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/ae476035cbf34e848053be9079e84615.png)

![在这里插入图片描述](https://img-blog.csdnimg.cn/1589d28707824e84b59e0bcaa32c5b17.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/336442387e7447cfa53cd1bf07ed0695.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/c3a2fdcd251a40dcbefe5c1daf4810fe.png)
![在这里插入图片描述](https://img-blog.csdnimg.cn/25d89dc344ed4c518e8192559242e1d0.png)


#### 模型和数据文件
受限于文件大小，本项目并未上传模型和数据文件。在训练本项目的模型文件时，做了二分类和逻辑回归两种实验条件下的训练，模型最终在测试集上的结果如下：

二分类
|模型|	Total|	Correct|	ACC|	AUC|
|--|--|--|--|--|
|DSSM(user)|	1373344|	857725|	0.62455|	0.7312|
|DSSM(item)|	1373344|	857725|	0.62455|	0.7306|
|DeepFM|	1373344|	858895|	0.6254	|0.73428|

逻辑回归
|模型	|Total|	Correct|	ACC|	MAE|
|--|--|--|--|--|
|DSSM(user)|	1373344|	797789|	0.58090|	2.57662|
|DSSM(item)	|1373344	|798387	|0.58134|	2.56567|
|DeepFM	|1373344	|765238	|0.55720	|2.43759|

DSSM模型的ACC最高提升了7.5%，DeepFM模型的ACC最高提升了12.24%。

如果您需要训练自己的模型文件，可以参考[官方项目](https://aistudio.baidu.com/aistudio/projectdetail/1481839)或[我的项目](https://aistudio.baidu.com/aistudio/projectdetail/3370104)自己训练获取模型或者完成一个新的推荐系统，或者私信我获取本项目缺少的模型和对应的数据文件

#### 致谢
>项目遵守[Apache License 2.0](http://www.apache.org/licenses/)协议，将代码更改的部分已作说明非常感谢[PaddleRec](https://github.com/PaddlePaddle/PaddleRec)的demo，本项目大部分是基于该项目部分改动得到的。
感谢[京东2019用户对品类下店铺的购买预测竞赛数据集](https://jdata.jd.com/html/detail.html?id=8)
感谢[PaddleServing](https://github.com/PaddlePaddle/Serving)、[Redis](https://github.com/Redis)、[milvus](https://github.com/milvus-io/milvus)对项目部署的支持；
感谢[Protobuf](https://github.com/protocolbuffers/protobuf)和[gRPC](https://github.com/grpc/grpc)，实现了本项目的服务模块分布式部署和通信。
