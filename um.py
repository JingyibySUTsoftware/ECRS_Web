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

from proto import um_pb2 
from proto import um_pb2_grpc 
from proto import user_info_pb2 as user_info_pb2
import redis
import json

#实现服务的接口
class UMServerServicer(object):
    def __init__(self):
        self.redis_cli = redis.StrictRedis(host="127.0.0.1", port="6379")
    #该方法接受用户id，在redis中查询对应用户信息
    def um_call(self, request, context):
        '''
        message UserModelRequest {
            string log_id = 1;
            string user_id = 2;
        };
        '''
        um_res = um_pb2.UserModelResponse()
        user_id = request.user_id;
        redis_res = self.redis_cli.get("{}##user_info".format(user_id))
        if redis_res is None:
            um_res.error.code = 500
            um_res.error.text = "UM server get user_info from redis fail. ({})".format(str(request))
            return um_res
            #raise ValueError("UM server get user_info from redis fail. ({})".format(str(request)))
        um_res.error.code = 200
        user_info = json.loads(redis_res)
        '''
        user_info = {"user_id": user_id,
                "age": age,
                "sex": sex,
                "city_level": city_level,
                "province": province,
                "city": city,
                "country": country
                }
        '''
        um_res.user_info.user_id = user_info["user_id"]
        um_res.user_info.age = user_info["age"]
        um_res.user_info.sex = user_info["sex"]
        um_res.user_info.city_level = user_info["city_level"]
        um_res.user_info.province = user_info["province"]
        um_res.user_info.city = user_info["city"]
        um_res.user_info.country = user_info["country"]
        return um_res
#定义服务
class UMServer(object):
    """
    um server
    """
    #开启服务，对外提供rpc调用
    def start_server(self):
        max_workers = 40#定义多线程的服务器对象
        concurrency = 40#定义最大连接数量
        port = 8910#定义服务端口
        
        #创建服务对象
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            options=[('grpc.max_send_message_length', 1024 * 1024),
                     ('grpc.max_receive_message_length', 1024 * 1024)],
            maximum_concurrent_rpcs=concurrency)
        #注册实现服务的方法到服务器对象中
        servicer = UMServerServicer()
        um_pb2_grpc.add_UMServiceServicer_to_server(servicer, server)
        #为服务绑定主机与端口
        server.add_insecure_port('[::]:{}'.format(port))
        #开启服务
        server.start()
        print('um服务已开启！')
        server.wait_for_termination()

if __name__ == "__main__":
    um = UMServer()
    um.start_server()
