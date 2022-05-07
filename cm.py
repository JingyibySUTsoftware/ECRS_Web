#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# !/bin/env python

from __future__ import unicode_literals

from concurrent import futures

import grpc

from proto import cm_pb2 
from proto import cm_pb2_grpc 
from proto import item_info_pb2 as item_info_pb2
import redis
import json

#实现服务的接口
class CMServerServicer(object):
    def __init__(self):
        self.redis_cli = redis.StrictRedis(host="127.0.0.1", port="6379")
    #通过商品的一个或多个id在redis中查找对应的商品信息
    def cm_call(self, request, context):
        cm_res = cm_pb2.CMResponse()
        item_ids = request.item_ids;
        for item_id in item_ids:
            redis_res = self.redis_cli.get("{}##product_info".format(item_id))
            if redis_res is None:
                cm_res.error.code = 500
                cm_res.error.text = "CM server get item_info from redis fail. ({})".format(str(request))
                return cm_res
                #raise ValueError("CM server get user_info from redis fail. ({})".format(str(request)))
            cm_info = json.loads(redis_res)
            item_info = cm_res.item_infos.add()

            '''
            product_info = {"sku_id" : sku_id,
                "brand" : brand,
                "shopid" : shopid,
                "cate" : cate
                }
            '''
            if "sku_id" not in cm_info:
                raise ValueError("not get product from cm")
            item_info.sku_id = cm_info["sku_id"]
            item_info.brand = cm_info["brand"]
            item_info.shopid = cm_info["shopid"]
            item_info.cate = cm_info["cate"]
        cm_res.error.code = 200
        return cm_res
#定义服务
class CMServer(object):
    """
    cm server
    """
    #开启服务，对外提供rpc调用
    def start_server(self):
        max_workers = 40  # 定义多线程的服务器对象
        concurrency = 40  # 定义最大连接数量
        port = 8920  # 定义服务端口
        #创建服务对象
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            options=[('grpc.max_send_message_length', 1024 * 1024),
                     ('grpc.max_receive_message_length', 1024 * 1024)],
            maximum_concurrent_rpcs=concurrency)
        servicer = CMServerServicer()
        #注册实现服务的方法到服务器对象中
        cm_pb2_grpc.add_CMServiceServicer_to_server(servicer, server)
        #为服务绑定主机与端口
        server.add_insecure_port('[::]:{}'.format(port))
        #开启服务
        server.start()
        print('cm服务已开启！')
        server.wait_for_termination()

if __name__ == "__main__":
    um = CMServer()
    um.start_server()
