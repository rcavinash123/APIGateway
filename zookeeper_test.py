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
    if zk.exists("/apigateway"):
        print("API Gateway Existis")
        #data = json.dumps({"endpoints":{"url":"http://192.168.200.148:30838"}})
        #zk.set("/apigateway",data)
        data = zk.get("/apigateway")
        print(str(data))
        zk.stop()
    else:
        print("Node doesn not exists")
except Exception as err:
    print("Cannot connect to zookeeper : " + str(err))


