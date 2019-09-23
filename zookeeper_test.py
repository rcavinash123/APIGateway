from kazoo.client import KazooClient
import json
import requests
import logging
import sys

logging.basicConfig()


try:
    zk = KazooClient(hosts='192.168.200.198:4184,192.168.200.197:4184')
    zk.start()
    print("Starting Zoo Keeper")
    if zk.exists("/microservices/authservice"):
        data = zk.get("/microservices/authservice")
        data = json.dumps(data)
        jsonData = json.loads(data)
        Data = jsonData[0]
        JsonData = json.loads(Data)
        print("AuthURL : " + str(JsonData["authservice"]["url"]))
        zk.stop()
    else:
        print("Node doesn not exists")
except Exception as err:
    print("Cannot connect to zookeeper : " + str(err))


