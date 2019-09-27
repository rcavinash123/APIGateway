from kazoo.client import KazooClient
import json
import requests
import logging
import sys
from pymongo import MongoClient

logging.basicConfig()


try:
    zk = KazooClient(hosts='192.168.200.198:4184,192.168.200.197:4184')
    zk.start()
    print("Starting Zoo Keeper")
    if zk.exists("/databases/mongodb"):
        print("API Gateway Existis")
        #data = json.dumps({"endpoints":{"url":"mongodb://192.168.200.197:27017","username":"root","password":"uAJveH3wFlFkj+Um"}})
        #zk.set("/databases/mongodb",data)
        data = zk.get("/databases/mongodb")
        data = json.loads(data[0])
        print("MongoString : " + str(data["endpoints"]["url"]))
        zk.stop()

        client = MongoClient(data["endpoints"]["url"],username=data["endpoints"]["username"],password=data["endpoints"]["password"])
        mongodb = client.CubusDBTest
        users = mongodb.users
        user = users.find_one({'userName' : 'cubusdemo','password':'@Cu2010bus'})
        print("ID is : " + str(user['_id']))

    else:
        print("Node doesn not exists")

except Exception as err:
    print("Cannot connect to zookeeper : " + str(err))


