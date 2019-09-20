from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from kazoo.client import KazooClient
import json
import requests
import random
from requests.exceptions import HTTPError
import config
import logging

logging.basicConfig()

app = Flask(__name__)

@app.route('/auth/healthz',methods=['GET'])
def healthResponse():
    try:
        zk = KazooClient(hosts=config.ZOOKEEPER_HOST,timeout=5,max_retries=3)
        zk.start()
        data = json.dumps({"endpoints":{"url":"http://apigateway.default.svc.cluster.local:4001"}})
        if zk.exists("/apigateway"):
            zk.set("/apigateway",data)
        else:
            zk.create("/apigateway",data)
        jresp = json.dumps({"status":"pass"})
        resp = Response(jresp, status=200, mimetype='application/json')
        return resp
    except:
        print('Failed to connect to zookeeper')
        jresp = json.dumps({"status":"fail","reason":"Failed to connect to zookeeper"})
        resp = Response(jresp, status=500, mimetype='application/json')
        return resp

@app.route('/auth/validate/<userName>/<password>',methods=['POST'])
def userValidate(userName,password):
    zk = KazooClient(hosts=config.ZOOKEEPER_HOST)
    zk.start()
    services = []
    if zk.exists("/microservices/authService"):
        data = zk.get("/microservices/authService")
        jsonData = json.loads(data.decode('utf-8'))
        authURL = jsonData["endpoints"]["url"]
        try:
            authResponse = requests.post(userName,password)
        except HTTPError as http_err:
            jsonData = json.dumps({"status":"Failed","code":"500","reason":str(http_err)})
            resp = Response(jsonData,status=200)
            return resp 
        except Exception as err:
            jsonData = json.dumps({"status":"Failed","code":"500","reason":str(err)})
            resp = Response(jsonData,status=200)
            return resp
        else:
            if authResponse:
                return authResponse
            else:
                jsonData = json.dumps({"status":"Failed","code":"500","reason":"Recieved empty response from the service"})
                authResponse = Response(jsonData,status=200)
                return authResponse
    else:
        jsonData = json.dumps({"status":"Failed","code":"500","reason":"Node does not exists"})
        resp = Response(jsonData,status=200)
        return resp

if __name__ == '__main__':
    app.run(debug=config.DEBUG_MODE,host='0.0.0.0',port=config.PORT)