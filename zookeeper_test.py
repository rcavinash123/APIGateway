from kazoo.client import KazooClient
import json
import requests
import logging
import sys
from pymongo import MongoClient
import redis

logging.basicConfig()


try:
    zk = KazooClient(hosts='192.168.200.182:2181')
    zk.start()
    print("Starting Zoo Keeper")
    if zk.exists("/databases/redisdb"):
        print("RedisDB Exists")
        
        #data = json.dumps({"endpoints":{"url":"mongodb://192.168.200.182:27017","username":"","password":""}})
        #zk.set("/databases/mongodb",data)
        #zk.stop()

        data = json.dumps({"endpoints":{"host":"192.168.200.182","port":"6379","password":""}})
        zk.set("/databases/redisdb",data)

        #data = zk.get("/databases/redisdb")
        #data = json.loads(data[0])
        #print("Host : " + str(data["endpoints"]["host"]))
        #print("Port : " + str(data["endpoints"]["port"]))
        #print("Password : " + str(data["endpoints"]["password"]))

        #print("Able to access zookeeper successfully")
        #zk.stop()

        #client = MongoClient(data["endpoints"]["url"],username=data["endpoints"]["username"],password=data["endpoints"]["password"])
        #client = MongoClient("mongodb://192.168.200.182:27017",username="",password="")
        #mongodb = client.CubusDBTest
        #users = mongodb.users
        #user = users.find_one({'userName' : 'cubusdemo','password':'@Cu2010bus'})
        #print("ID is : " + str(user['_id']))
    
        #redisdb = redis.Redis(host="192.168.200.182",port="6379",password="")
        #redisdb.ping()
        #redisdb.setex(str("1"),80,"{ 'value':'Test Data' }")
        #print("Data : " + redisdb.get("1"))
    else:
        print("Node does not exists")
except Exception as err:
    print("Cannot connect to zookeeper : " + str(err))


