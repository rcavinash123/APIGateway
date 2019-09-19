from kazoo.client import KazooClient
import json
import requests

zk = KazooClient(hosts='172.17.0.2:2181')
zk.start()

if zk.exists("/microservices"):
    print("MicroServices Exists")
else:
    print("Microservices Not Exists")