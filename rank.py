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

from proto import rank_pb2 
from proto import rank_pb2_grpc 
from proto import user_info_pb2 as user_info_pb2
import redis

import numpy as np
from paddle_serving_app.local_predict import LocalPredictor
def hash2(a):
    return hash(a) % 20000000
#实现服务的接口
class RankServerServicer(object):
    def __init__(self):
        #加载排序模型
        self.ctr_client = LocalPredictor()
        self.ctr_client.load_model_config("rank_model")
    #处理需要输入到模型中的数据
    def process_feed_dict(self, user_info, item_infos):
        #" user_id age sex city_level province city country | sku_id brand shopid cate"
        '''
            item_info.sku_id = cm_info["sku_id"]
            item_info.brand = cm_info["brand"]
            item_info.shopid = cm_info["shopid"]
            item_info.cate = cm_info["cate"]

            um_res.user_info.user_id = user_info["user_id"]
            um_res.user_info.age = user_info["age"]
            um_res.user_info.sex = user_info["sex"]
            um_res.user_info.city_level = user_info["city_level"]
            um_res.user_info.province = user_info["province"]
            um_res.user_info.city = user_info["city"]
            um_res.user_info.country = user_info["country"]    
        '''
        dic = {"userid": [], "age": [], "sex": [], "city_level": [], "province": [], "city": [], "country": [], "sku_id": [], "brand": [], "shopid": [], "cate": []}
        batch_size = len(item_infos)
        lod = [0]
        for i, item_info in enumerate(item_infos):
            dic["sku_id"].append(hash2(item_info.sku_id))
            dic["brand"].append(hash2(item_info.brand))
            dic["shopid"].append(hash2(item_info.shopid))
            dic["cate"].append(hash2(item_info.cate))
            dic["userid"].append(hash2(user_info.user_id))
            dic["age"].append(hash2(user_info.age))
            dic["sex"].append(hash2(user_info.sex))
            dic["city_level"].append(hash2(user_info.city_level))
            dic["province"].append(hash2(user_info.province))
            dic["city"].append(hash2(user_info.city))
            dic["country"].append(hash2(user_info.country))
            lod.append(i+1)

        dic["sku_id.lod"] = lod
        dic["brand.lod"] = lod
        dic["shopid.lod"] = lod
        dic["cate.lod"] = lod
        dic["userid.lod"] = lod
        dic["age.lod"] = lod
        dic["sex.lod"] = lod
        dic["city_level.lod"] = lod
        dic["province.lod"] = lod
        dic["city.lod"] = lod
        dic["country.lod"] = lod
        for key in dic:
            dic[key] = np.array(dic[key]).astype(np.int64).reshape(len(dic[key]),1)

        return dic
    #排序服务，对用户和商品信息做更精细的打分
    def rank_predict(self, request, context):
        '''
        message RankRequest {
          string log_id = 1;
            user_info.UserInfo user_info = 2;
            repeated item_info.ItemInfo item_infos = 3;
        }

        message RankResponse {
            message Error {
                uint32 code = 1;
                string text = 2;
            }
            message ScorePair {
                string nid = 1;
                float score = 2;
            };
            Error error = 1;
            repeated ScorePair score_pairs = 2;
        };
        '''
        batch_size = len(request.item_infos)
        dic = self.process_feed_dict(request.user_info, request.item_infos)
        #paddleServing模型推理服务，如果您更换了模型请在此处更改参数
        fetch_map = self.ctr_client.predict(feed=dic, fetch=["save_infer_model/scale_0.tmp_6"], batch=True)
        response = rank_pb2.RankResponse()
        
        #raise ValueError("UM server get user_info from redis fail. ({})".format(str(request)))
        response.error.code = 200

        for i in range(batch_size):
            score_pair = response.score_pairs.add()
            score_pair.nid = request.item_infos[i].sku_id
            score_pair.score = fetch_map["save_infer_model/scale_0.tmp_6"][i][0]#通过rank模型预测打分
        response.score_pairs.sort(reverse=True, key = lambda item: item.score)#逆序得分
        return response
#定义服务
class RankServer(object):
    """
    rank server
    """
    #开启服务，对外提供rpc调用
    def start_server(self):
        max_workers = 40#定义多线程的服务器对象
        concurrency = 40#定义最大连接数量
        port = 8960  # 定义服务端口
        #创建服务对象
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            options=[('grpc.max_send_message_length', 1024 * 1024),
                     ('grpc.max_receive_message_length', 1024 * 1024)],
            maximum_concurrent_rpcs=concurrency)
        #注册实现服务的方法到服务器对象中
        servicer = RankServerServicer()
        rank_pb2_grpc.add_RankServiceServicer_to_server(servicer, server)
        #为服务绑定主机与端口
        server.add_insecure_port('[::]:{}'.format(port))
        #开启服务
        server.start()
        print('rank服务已启动！')
        server.wait_for_termination()

if __name__ == "__main__":
    rank = RankServer()
    rank.start_server()
