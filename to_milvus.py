import random
# from pprint import pprint

# from milvus import Milvus, DataType
#
# _HOST = '127.0.0.1'
# _PORT = '19530'
# client = Milvus(_HOST, _PORT)
#

#
# if collection_name in client.list_collections():
#     client.drop_collection(collection_name)
#
# collection_param = {
#     "fields": [
#         # {"name": "id", "type": DataType.INT32},
#         {"name": "embedding", "type": DataType.FLOAT_VECTOR, "params": {"dim": 32}},
#     ],
#     "segment_row_limit": 16384,
#     "auto_id": False
# }
#
# client.create_collection(collection_name, collection_param)
# client.create_partition(collection_name, "Movie")
#
# print("--------get collection info--------")
# collection = client.get_collection_info(collection_name)
# pprint(collection)
# partitions = client.list_partitions(collection_name)
# print("\n----------list partitions----------")
# pprint(partitions)
# ids = client.insert()


import codecs

import sys
sys.path.append("milvus_tool")

from milvus_tool.milvus_insert import VecToMilvus


def get_vectors():
    with codecs.open("product_vectors.txt", "r", encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    ids = [int(line.split(":")[0]) for line in lines]
    embeddings = []
    for line in lines:
        line = line.strip().split(":")[1][1:-1]
        str_nums = line.split(",")
        emb = [float(x) for x in str_nums]
        embeddings.append(emb)
    return ids, embeddings


ids, embeddings = get_vectors()

collection_name = 'demo_e_commerce'
client = VecToMilvus()
status, ids = client.insert(collection_name=collection_name, vectors=embeddings, ids=ids, partition_tag="Product")