import redis
import json
import codecs

#["sku_id", "brand", "shopid","cate"]
#1:3456:6980:70
def process_product(lines, redis_cli):
    for line in lines:
        if len(line.strip()) == 0:
            continue
        tmp = line.strip().split(":")
        sku_id = tmp[0]
        brand = tmp[1]
        shopid = tmp[2]
        cate=tmp[3]
        
        product_info = {"sku_id" : sku_id,
                "brand" : brand,
                "shopid" : shopid,
                "cate" : cate
                }
        redis_cli.set("{}##product_info".format(sku_id), json.dumps(product_info))

#["userid", "age", "sex", "city_level","province","city","country"]
#1:5.0:1.0:5.0:20.0:176.0:1933.0
def process_user(lines, redis_cli):
    for line in lines:
        if len(line.strip()) == 0:
            continue
        tmp = line.strip().split(":")
        user_id = tmp[0]
        age = tmp[1]
        sex = tmp[2]
        city_level = tmp[3]
        province = tmp[4]
        city = tmp[5]
        country = tmp[6]

        user_info = {"user_id": user_id,
                "age": age,
                "sex": sex,
                "city_level": city_level,
                "province": province,
                "city": city,
                "country": country
                }
        redis_cli.set("{}##user_info".format(user_id), json.dumps(user_info))

if __name__ == "__main__":
    r = redis.StrictRedis(host="127.0.0.1", port="6379") 
    with codecs.open("users.dat", "r",encoding='utf-8',errors='ignore') as f:
        lines = f.readlines()
        process_user(lines, r)
    with codecs.open("products.dat", "r",encoding='utf-8',errors='ignore') as f:
        lines = f.readlines()
        process_product(lines, r)