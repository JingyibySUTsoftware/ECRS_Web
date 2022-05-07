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

import sys
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


def get_ums(uid):
    channel = grpc.insecure_channel('127.0.0.1:8910')
    stub = um_pb2_grpc.UMServiceStub(channel)
    request = um_pb2.UserModelRequest()
    request.user_id = str(uid)
    response = stub.um_call(request)
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


def get_as(request):
    channel = grpc.insecure_channel("127.0.0.1:8930")
    stub = as_pb2_grpc.ASServiceStub(channel)
    response = stub.as_call(request)
    return response


if __name__ == "__main__":
    if sys.argv[1] == 'as':
        start=time.process_time()
        req = as_pb2.ASRequest()
        if len(sys.argv) == 3:
            uid = sys.argv[2]
            req.user_id = uid
        else:
            age = sys.argv[2]
            sex = sys.argv[3]
            city_level = sys.argv[4]
            province = sys.argv[5]
            city = sys.argv[6]
            country = sys.argv[7]
            req.user_info.user_id, req.user_info.age, req.user_info.sex, req.user_info.city_level, req.user_info.province, req.user_info.city, req.user_info.country = "0", age, sex, city_level , province, city, country
        print(get_as(req))
        end=time.process_time()
        print('as service response time:'+str(end-start))
    if sys.argv[1] == 'um':
        start=time.process_time()
        uid = sys.argv[2]
        print(get_ums(uid))
        end=time.process_time()
        print('um service response time:'+str(end-start))
    if sys.argv[1] == 'cm':
        start=time.process_time()
        nid_list_str= sys.argv[2]
        nid_list = nid_list_str.strip().split(",")
        print(get_cm(nid_list))
        end=time.process_time()
        print('cm service response time:'+str(end-start))
    if sys.argv[1] == "recall":
        start=time.process_time()
        uid = sys.argv[2]
        user_info = get_ums(uid).user_info
        request = recall_pb2.RecallRequest()
        request.user_info.CopyFrom(user_info)
        print(get_recall(request))
        end=time.process_time()
        print('recall service response time:'+str(end-start))
    if sys.argv[1] == "rank":
        start=time.process_time()
        request = rank_pb2.RankRequest()
        request.user_info.user_id= "1"
        request.user_info.age= "5.0" 
        request.user_info.sex= "1.0"
        request.user_info.city_level= "5.0"
        request.user_info.province= "20.0"
        request.user_info.city= "176.0" 
        request.user_info.country= "1933.0"
        item_info = request.item_infos.add()
        item_info.sku_id = "1"
        item_info.brand = "3456"
        item_info.shopid = "6980"
        item_info.cate = "70"
        print(get_rank(request))
        end=time.process_time()
        print('rank service response time:'+str(end-start))
