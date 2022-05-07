#   Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or aaseed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# !/bin/env python

from __future__ import unicode_literals

from concurrent import futures

import grpc

from proto import as_pb2
from proto import as_pb2_grpc
from proto import user_info_pb2 as user_info_pb2
from proto import item_info_pb2 as item_info_pb2
from proto import recall_pb2 as recall_pb2
from proto import recall_pb2_grpc as recall_pb2_grpc
from proto import rank_pb2 as rank_pb2
from proto import rank_pb2_grpc as rank_pb2_grpc
from proto import um_pb2 as um_pb2
from proto import um_pb2_grpc as um_pb2_grpc
from proto import cm_pb2 as cm_pb2
from proto import cm_pb2_grpc as cm_pb2_grpc
import redis


def get_ums(uid):
    channel = grpc.insecure_channel('127.0.0.1:8910')
    stub = um_pb2_grpc.UMServiceStub(channel)
    response = stub.um_call(um_pb2.UserModelRequest(user_id=str(uid).encode(encoding='utf-8')))
    return response

def get_recall(request):

    channel = grpc.insecure_channel('127.0.0.1:8950')
    stub = recall_pb2_grpc.RecallServiceStub(channel)
    response = stub.recall(request)
    return response

def get_cm(nid_list):
    channel = grpc.insecure_channel('127.0.0.1:8920')
    stub = cm_pb2_grpc.CMServiceStub(channel)
    cm_request = cm_pb2.CMRequest()
    for nid in nid_list:
        cm_request.item_ids.append(str(nid).encode(encoding='utf-8'))
    cm_response = stub.cm_call(cm_request,timeout=10)
    return cm_response

def get_rank(request):
    channel = grpc.insecure_channel('127.0.0.1:8960')
    stub = rank_pb2_grpc.RankServiceStub(channel)
    response = stub.rank_predict(request)
    return response
#实现服务的接口
class ASServerServicer(object):
    def __init__(self):
        pass
    #应用服务，将其他几个服务串联
    def as_call(self, request, context):
        '''
        message ASRequest{
          string log_id = 1;
          string user_id = 2;
          user_info.UserInfo user_info = 3;
        }
        message ASResponse {
            message Error {
                uint32 code = 1;
                string text = 2;
            }
            Error error = 1;
            repeated item_info.ItemInfo item_infos = 2;
        }
        message ItemInfo {
            string movie_id = 1;
            string title = 2;
            string genre = 3;
        }
        '''
        #获取用户id，在um服务查找用户信息，如果传过来的不是用户id，则把传过来的用户信息向recall服务传递
        recall_req = recall_pb2.RecallRequest()
        if request.user_id != "-1": 
            user_id = request.user_id
            um_res = get_ums(user_id)
            recall_req.user_info.CopyFrom(um_res.user_info)
        else:
            recall_req.user_info.CopyFrom(request.user_info)
        #recall服务通过用户信息，生成用户特征向量，使用该向量在milvus中召回相似度前100个商品id列表    
        recall_res = get_recall(recall_req)
        nid_list = [x.nid for x in recall_res.score_pairs]
        #cm服务通过这个商品id列表查找对应的商品信息
        cm_res = get_cm(nid_list) 
        item_dict = {}
        for x in cm_res.item_infos:
            item_dict[x.sku_id] = x
        #rank服务把用户信息与商品信息全部输入到rank模型中，服务返回商品id和对应得分
        rank_req = rank_pb2.RankRequest()
        rank_req.user_info.CopyFrom(um_res.user_info)
        rank_req.item_infos.extend(cm_res.item_infos)
        rank_res = get_rank(rank_req)
        #as服务根据rank服务传回来的结果重新拼接数据，返回完整的已逆序排好的商品信息
        as_res = as_pb2.ASResponse()
        as_res.error.code = 200
        for sp in rank_res.score_pairs:
            nid = sp.nid
            #这里选择开启在最终结果里添加评分结果 score=sp.score
            rankscore=sp.score
            item_info = item_dict[nid]
            item_info.rank_score=rankscore
            as_res.item_infos.extend([item_info])

        return as_res
#定义服务
class ASServer(object):
    """
    as server
    """
    #开启服务，对外提供rpc调用
    def start_server(self):
        max_workers = 40#定义多线程的服务器对象
        concurrency = 40  # 定义最大连接数量
        port = 8930  # 定义服务端口
        #创建服务对象
        server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=max_workers),
            options=[('grpc.max_send_message_length', 1024 * 1024),
                     ('grpc.max_receive_message_length', 1024 * 1024)],
            maximum_concurrent_rpcs=concurrency)
        #注册实现服务的方法到服务器对象中
        servicer = ASServerServicer()
        as_pb2_grpc.add_ASServiceServicer_to_server(servicer, server)
        #为服务绑定主机与端口
        server.add_insecure_port('[::]:{}'.format(port))
        #开启服务
        server.start()
        print('Application服务已启动！')
        server.wait_for_termination()

if __name__ == "__main__":
    As = ASServer()
    As.start_server()
