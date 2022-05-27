from contextlib import nullcontext
from mimetypes import init
from optparse import Values
import sys
from unittest import result
from urllib import response

from requests import request
import grpc
import proto.um_pb2 as um_pb2
import proto.um_pb2_grpc as um_pb2_grpc
import proto.cm_pb2 as cm_pb2
import proto.cm_pb2_grpc as cm_pb2_grpc
import proto.rank_pb2 as rank_pb2
import proto.rank_pb2_grpc as rank_pb2_grpc
import proto.recall_pb2 as recall_pb2
import proto.recall_pb2_grpc as recall_pb2_grpc
import proto.as_pb2 as as_pb2
import proto.as_pb2_grpc as as_pb2_grpc
import json
from google.protobuf.json_format import MessageToJson, Parse
import time
from flask import Flask, redirect, url_for, render_template
from flask import request as req
from flask_cache import Cache
import os
from client import get_cm, get_ums, get_recall, get_as, get_rank
from gevent.pywsgi import WSGIServer

basedirs = os.path.abspath(os.path.dirname(__file__))
basedir = basedirs + '/cache'
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'filesystem',
                           'CACHE_DIR': basedir})  # 开启Flask缓存

#默认起始页为登录页
@app.route('/')
@cache.cached(timeout=0)  # timeout为0表示缓存永久有效
def login():
    return render_template('login.html')

#登录之后跳转客户端演示使用，这里不做验证任意账号皆可登录
@app.route('/login', methods=['POST', 'GET'])
def afterlogin():
    user = req.form['username']
    #index.html仅适配PC端,newindex.html适配移动端+PC端，开发者可以自行替换体验
    return render_template('newindex.html', username=user)

#引导页
@app.route('/toStart')
@cache.cached(timeout=0)
def start():
    return render_template('start.html')

#404页面
@app.route('/error')
def error():
    render_template('404.html')

@app.errorhandler(404)  # 传入错误码作为参数状态
def error_404(e):
    return render_template("404.html"), 404  # 返回对应的http状态码，和返回404错误的html文件

#只要出现错误，都默认到404页面，这里我没有准备那么多的页面，您可以自由决定或者制作对应的错误页面
@app.errorhandler(500)
def error_500(e):
    return render_template("404.html"), 500

#跳转到um服务页面,并初始化
@app.route('/toUm')
@cache.cached(timeout=0)
def toUmService():
    init_list = ['无', '无', '无', '无', '无', '无', '无']
    init_uid = 0
    init_time = '无'
    init_originData = 0
    init_code = 100
    return render_template('umShow.html', result=init_list, uid=init_uid, costTime=init_time, originData=init_originData, stateCode=init_code)

#查找指定id的用户信息
@app.route('/umServer', methods=['GET', 'POST'])
def umService():
    #向um服务发送请求
    if req.method == 'GET':
        searchid = req.args.get('ToSearchUid')
    start = time.process_time()
    response = get_ums(searchid)
    end = time.process_time()
    #处理数据
    dict = pb2dict(response.user_info)
    statedict = pb2dict(response.error)
    values = list(dict.values())
    cost = str(end-start)
    if cost != "" and values != "":
        return render_template('umShow.html', uid=searchid, result=values, costTime=cost+'s', originData=response, stateCode=statedict['code'])
    else:
        return redirect(url_for('error'))

#跳转到cm服务页面,并初始化
@app.route('/toCm')
@cache.cached(timeout=0)
def toCmService():
    init_list = ['无', '无', '无', '无']
    init_sid = 0
    init_time = '无'
    init_originData = 0
    init_code = 100
    return render_template('cmShow.html', result=init_list, sku_id=init_sid, costTime=init_time, originData=init_originData, stateCode=init_code)

#查找指定id的商品信息
@app.route('/cmServer', methods=['GET', 'POST'])
def cmService():
    #向cm服务发送请求
    if req.method == 'GET':
        searchid = req.args.get('ToSearchSku_id')
    start = time.process_time()
    nid_list = searchid.strip().split("A")
    cm_response = get_cm(nid_list)
    end = time.process_time()
    #处理数据
    resultValue = []
    for item in cm_response.item_infos:
        dict = pb2dict(item)
        resultValue.append(dict)
    statedict = pb2dict(cm_response.error)
    cost = str(end-start)
    if cost != "" and resultValue != "":
        return render_template('cmShow.html', sku_id=searchid, result=resultValue, costTime=cost+'s', originData=cm_response, stateCode=statedict['code'])
    else:
        return redirect(url_for('error'))

#跳转到recall服务页面并初始化
@app.route('/toRecall')
@cache.cached(timeout=0)
def toRecallService():
    dict = {'nid': '无', 'score': '无'}
    init_list = [dict]
    init_uid = 0
    init_time = '无'
    init_originData = 0
    init_code = 100
    return render_template('recallShow.html', result=init_list, uid=init_uid, costTime=init_time, originData=init_originData, stateCode=init_code)
#召回指定id用户的商品候选集
@app.route('/recallServer')
def recallService():
    #向cm服务发送请求
    if req.method == 'GET':
        searchid = req.args.get('ToSearchUid')
    start = time.process_time()
    user_info = get_ums(searchid).user_info
    request = recall_pb2.RecallRequest()
    request.user_info.CopyFrom(user_info)
    response = get_recall(request)
    end = time.process_time()
    #处理数据
    resultValue = []
    for item in response.score_pairs:
        dict = pb2dict(item)
        resultValue.append(dict)
    statedict = pb2dict(response.error)
    cost = str(end-start)
    if cost != "" and resultValue != "":
        return render_template('recallShow.html', uid=searchid, result=resultValue, costTime=cost+'s', originData=response, stateCode=statedict['code'])
    else:
        return redirect(url_for('error'))
#跳转到rank服务页面并初始化
@app.route('/toRank')
@cache.cached(timeout=0)
def rankService():
    start = time.process_time()
    #rank服务需要其他模块配合执行，单独运行时，则使用以下默认参数
    request = rank_pb2.RankRequest()
    request.user_info.user_id = "1"
    request.user_info.age = "5.0"
    request.user_info.sex = "1.0"
    request.user_info.city_level = "5.0"
    request.user_info.province = "20.0"
    request.user_info.city = "176.0"
    request.user_info.country = "1933.0"
    item_info = request.item_infos.add()
    item_info.sku_id = "1"
    item_info.brand = "3456"
    item_info.shopid = "6980"
    item_info.cate = "70"
    response = get_rank(request)
    end = time.process_time()
    #处理数据
    resultValue = []
    for item in response.score_pairs:
        dict = pb2dict(item)
        resultValue.append(dict)
    statedict = pb2dict(response.error)
    cost = str(end-start)
    if cost != "" and resultValue != "":
        return render_template('rankShow.html', result=resultValue, costTime=cost+'s', originData=response, stateCode=statedict['code'])
    else:
        return redirect(url_for('error'))
#跳转到as服务页面并初始化
@app.route('/toAS')
@cache.cached(timeout=0)
def toAService():
    dict = {'sku_id': '无', 'brand': '无',
            'shopid': '无', 'cate': '无', 'rank_score': '无'}
    init_list = [dict]
    dict2 = {'sku_id': '无', 'brand': '无',
             'shopid': '无', 'cate': '无', 'rank_score': '无'}
    init_list2 = [dict2]
    init_uid = 0
    init_time = '无'
    init_time2 = '无'
    init_originData = 0
    init_originData2 = 0
    init_code = 100
    init_code2 = 100
    init_ageValue = 0
    init_sexValue = -1
    init_cityLevelValue = 0
    init_provinceVal = 0
    init_cityVal = 0
    init_countryVal = 0
    return render_template('asShow.html', result=init_list, result2=init_list2, uid=init_uid, costTime=init_time, costTime2=init_time2,
                           originData=init_originData, originData2=init_originData2, stateCode=init_code, stateCode2=init_code2, ageValue=init_ageValue, sexValue=init_sexValue,
                           cityLevelValue=init_cityLevelValue, provinceVal=init_provinceVal, cityVal=init_cityVal,
                           countryVal=init_countryVal)

#为新用户或老用户进行推荐
@app.route('/applicationServer', methods=['GET', 'POST'])
def ApplicationService():
    start = time.process_time()
    request = as_pb2.ASRequest()
    if req.method == 'GET':
        searchid = req.args.get('ToSearchUid')
        request.user_id = searchid
    if req.method == 'POST':
        age = req.form['age']
        sex = req.form['sex']
        city_level = req.form['city_level']
        province = req.form['province']
        city = req.form['city']
        country = req.form['country']
        request.user_info.user_id, request.user_info.age, request.user_info.sex, request.user_info.city_level, request.user_info.province, request.user_info.city, request.user_info.country = "0", age, sex, city_level, province, city, country
    response = get_as(request)
    end = time.process_time()
    #处理数据
    resultValue = []
    for item in response.item_infos:
        dict = pb2dict(item)
        resultValue.append(dict)
    statedict = pb2dict(response.error)
    cost = str(end-start)
    if cost != "" and resultValue != "" and req.method == 'POST':
        return render_template('asShow.html', uid=0, result2=resultValue, costTime2=cost+'s',
                               originData2=response, stateCode2=statedict['code'], ageValue=age, sexValue=sex,
                               cityLevelValue=city_level, provinceVal=province, cityVal=city,
                               countryVal=country, result=[{'sku_id': '无', 'brand': '无', 'shopid': '无', 'cate': '无', 'rank_score': '无'}], costTime='无',
                               originData=0, stateCode=100)
    elif cost != "" and resultValue != "" and req.method == 'GET':
        return render_template('asShow.html', uid=searchid, result=resultValue, costTime=cost+'s',
                               originData=response, stateCode=statedict['code'], ageValue=0, sexValue=-1,
                               cityLevelValue=0, provinceVal=0, cityVal=0,
                               countryVal=0, result2=[{'sku_id': '无', 'brand': '无', 'shopid': '无', 'cate': '无', 'rank_score': '无'}],
                               costTime2='无', originData2=0, stateCode2=100)
    else:
        return redirect(url_for('error'))
#跳转到关于页面
@app.route('/toabout')
@cache.cached(timeout=0)
def toAboutPage():
    return render_template('aboutShow.html')
#将message结构数据反序列化为字典格式
def pb2dict(obj):
    adict = {}
    if not obj.IsInitialized():
        return None

    for field in obj.DESCRIPTOR.fields:
        if not getattr(obj, field.name):
            continue
        from google.protobuf.descriptor import FieldDescriptor
        if not field.label == FieldDescriptor.LABEL_REPEATED:
            if not field.type == FieldDescriptor.TYPE_MESSAGE:
                adict[field.name] = getattr(obj, field.name)
            else:
                value = pb2dict(getattr(obj, field.name))
                if value:
                    adict[field.name] = value
        else:
            if field.type == FieldDescriptor.TYPE_MESSAGE:
                adict[field.name] = [pb2dict(v)
                                     for v in getattr(obj, field.name)]
            else:
                adict[field.name] = [v for v in getattr(obj, field.name)]
    return adict


if __name__ == '__main__':
    #gevent实现python异步协程
    WSGIServer(('127.0.0.1', 5001), app).serve_forever()
    #app.run()
