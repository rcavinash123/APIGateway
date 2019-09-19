from kazoo.client import KazooClient
import json
import requests

try:
    zk = KazooClient(hosts='192.168.200.197:2181')
    zk.start()
    if zk.exists("/microservices"):
        print("MicroServices Exists")
    else:
        print("Microservices Not Exists")
        zk.create("/microservices","")
except:
    print("Cannot connect to zookeeper")

