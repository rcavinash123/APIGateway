from kazoo.client import KazooClient
import json
import requests
import logging
logging.basicConfig()

try:
    zk = KazooClient(hosts='192.168.200.197:4184')
    zk.start()
    if zk.exists("/microservices"):
        print("MicroServices Exists")
    else:
        print("Microservices Not Exists")
        zk.create("/microservices","")
except:
    print("Cannot connect to zookeeper")

