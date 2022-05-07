import os
from milvus import MetricType, IndexType

MILVUS_HOST = '127.0.0.1'#ip
MILVUS_PORT = 19530#端口

collection_param = {
    'dimension': 32,#向量维度
    'index_file_size': 2048,#索引文件大小
    'metric_type': MetricType.L2#向量相似度计算方法，欧氏距离为L2，内积为IP
}
'''
1) 当查询数据规模小，且需要100％查询召回率时，用FLAT；

2) 当需要高性能查询，且要求召回率尽可能高时，用IVFFLAT；

3) 当需要高性能查询，且磁盘、内存、显存资源有限时，用IVFSQ8H；

4) 当需要高性能查询，且磁盘、内存资源有限，且只有CPU资源时，用IVFSQ8。

'''
index_type = IndexType.IVF_FLAT  # 索引类型有FLAT、IVFFLAT、IVFSQ8、IVFSQ8H
index_param = {'nlist': 1000}#聚类时总的分桶数

top_k = 100#召回的向量数
# 查询时需要搜索的分桶数目，谨慎更改，该参数会影响查询的性能和召回率,nprobe越大，召回率越高，但查询时间越长
search_param = {'nprobe': 100}

