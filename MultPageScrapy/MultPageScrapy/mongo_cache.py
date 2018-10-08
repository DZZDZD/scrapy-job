import pickle   #对象序列化
import zlib  #压缩数据
from datetime import datetime,timedelta   #设置缓存超时间隔
from pymongo import MongoClient
from bson.binary import Binary  #MongoDB存储二进制的类型

class MongoCache(object):
    """
    数据库缓存
    """
    def __init__(self,client=None,expires=timedelta(days=30)):  #timedelta 设置时间间隔
        """
        初始化函数
        :param client:数据库连接
        :param expires:超时时间
        """
        self.clinet = MongoClient('localhost',27017)
        self.db = self.clinet.zhilian  #创建一个名为zhilian的数据库
        web_page = self.db.webpage   #获取webpage这个集合（表 collection）

        #创建tiemstamp索引，设置超时时间为30天（转化为秒）
        self.db.webpage.create_index('timestamp',expireAfterSeconds=expires.total_seconds())

    def __setitem__(self, key, value):
        """
        向数据库添加一条缓存(数据)
        :param key: 缓存的键    传需要下载的页面网址
        :param value: 值    传下载后的页面内容
        :return:
        """
        #将数据使用pickle序列化,再使用zlib压缩且转换为Binary格式，使用格林威治时间
        record = {"result":Binary(zlib.compress(pickle.dumps(value))),"timestamp":datetime.utcnow()}
        #使用下载url作为key，存入系统默认生成_id字段，存入数据库
        self.db.webpage.update({"_id":key},{"$set":record},upsert=True)

    def __getitem__(self, item):
        """
        将缓存数据按照item作为key取出（key仍是下载的url）
        :param item:
        :return:
        """
        record = self.db.webpage.find_one({"_id":item})
        if record:
            a = pickle.loads(zlib.decompress(record["result"]))
            # return a.decode()
            return a
        else:
            raise  KeyError(item + "  does not exist")



    def __contains__(self, item):
        """
        当使用in，not in  会调用该方法判断链接对应的网址是否在数据库中
        :param item: 下载的url链接
        :return:
        """
        try:
            self[item]
        except KeyError:
            return False
        else:
            return True




    def clear(self):
        self.db.webpage.drop()


