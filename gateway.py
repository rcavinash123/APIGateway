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
        jresp = json.dumps({"result":{"status":"true","code":"200"}})
        zk.stop()
        resp = Response(jresp, status=200, mimetype='application/json')
        return resp
    except:
        print('Failed to connect to zookeeper')
        jresp = jsonifyumps({"result":{"status":"false","code":"500","reason":"Failed to connect to zookeeper"}})
        resp = Response(jresp, status=500, mimetype='application/json')
        return resp

@app.route('/auth/validate/<userName>/<password>',methods=['POST'])
def userValidate(userName,password):
    zk = KazooClient(hosts=config.ZOOKEEPER_HOST)
    zk.start()
    services = []
    if zk.exists("/microservices/authservice"):
        data = zk.get("/microservices/authservice")
        data = json.dumps(data)
        jsonData = json.loads(data)
        Data = jsonData[0]
        JsonData = json.loads(Data)
        authURL = str(JsonData["authservice"]["url"])

        #authURL = "http://0.0.0.0:4002/auth/validate/"

        try:
            authResponse = requests.post(authURL + userName + "/" + password)
        except HTTPError as http_err:
            jsonData = jsonify({"result":{"status":"false","code":"500","reason":str(http_err)}})
            resp = Response(jsonData,status=200,content_type="application/json")
            zk.stop()
            return resp 
        except Exception as err:
            jsonData = jsonify({"result":{"status":"false","code":"500","reason":str(err)}})
            resp = Response(jsonData,status=200)
            zk.stop()
            return resp
        else:
            if authResponse:
                zk.stop()
                return Response(authResponse,status=200,content_type="application/json")
            else:
                jsonData = jsonify({"result":{"status":"false","code":"500","reason":"Recieved empty response from the service"}})
                authResponse = Response(jsonData,status=200,content_type="application/json")
                zk.stop()
                return authResponse
    else:
        jsonData = jsonify({"result":{"status":"false","code":"500","reason":"Node does not exists"}})
        resp = Response(jsonData,status=200,content_type="application/json")
        zk.stop()
        return resp

@app.route('/userprofile/userprofileget/<ID>',methods=['GET'])
def userProfileGet(ID):
    zk = KazooClient(hosts=config.ZOOKEEPER_HOST)
    zk.start()
    services = []
    if zk.exists("/microservices/profileservice"):
        data = zk.get("/microservices/profileservice")
        data = json.dumps(data)
        jsonData = json.loads(data)
        Data = jsonData[0]
        JsonData = json.loads(Data)
        profileURL = str(JsonData["profileget"]["url"])

        #profileURL = "http://0.0.0.0:4003/userprofile/userprofileget/"

        try:
            profileResp = requests.get(profileURL + ID)
        except HTTPError as http_err:
            jsonData = jsonify({"result":{"status":"false","code":"500","reason":str(http_err)}})
            zk.stop()
            return Response(jsonData,200,content_type="application/json")
        except Exception as err:
            jsonData = jsonify({"result":{"status":"false","code":"500","reason":str(err)}})
            #resp = flask.Response(jsonData,status=200)
            zk.stop()
            return Response(jsonData,200,content_type="application/json")
        else:
            if profileResp:
                profileResp = Response(profileResp,status=200,content_type="application/json")
                zk.stop()
                return profileResp
            else:
                jsonData = jsonify({"result":{"status":"false","code":"500","reason":"Recieved empty response from the service"}})
                #Response = Response(jsonData,status=200)
                zk.stop()
                return Response(jsonData,200,content_type="application/json")
    else:
        jsonData = jsonify({"result":{"status":"false","code":"500","reason":"Node does not exists"}})
        #resp = Response(jsonData,status=200)
        zk.stop()
        return Response(jsonData,200,content_type="application/json")

@app.route('/userprofile/userprofileupdate/<Id>/<firstName>/<lastName>/<emailAddr>',methods=['POST'])
def userProfileUpdate(Id,firstName,lastName,emailAddr):
    zk = KazooClient(hosts=config.ZOOKEEPER_HOST)
    zk.start()
    services = []
    if zk.exists("/microservices/profileservice"):
        data = zk.get("/microservices/profileservice")
        data = json.dumps(data)
        jsonData = json.loads(data)
        Data = jsonData[0]
        JsonData = json.loads(Data)
        profileURL = str(JsonData["profileupdate"]["url"])
        try:
            profileResp = requests.post(profileURL + ID + "/" + firstName + "/" + lastName + "/" + emailAddr)
        except HTTPError as http_err:
            jsonData = jsonify({"result":{"status":"false","code":"500","reason":str(http_err)}})
            #resp = Response(jsonData,status=200)
            zk.stop()
            return Response(jsonData,200,content_type="application/json")
        except Exception as err:
            jsonData = jsonifyumps({"result":{"status":"false","code":"500","reason":str(err)}})
            #resp = Response(jsonData,status=200)
            zk.stop()
            return Response(jsonData,200,content_type="application/json")
        else:
            if profileResp:
                profileResp = Response(profileResp,status=200,content_type="application/json")
                zk.stop()
                return Response
            else:
                jsonData = jsonify({"result":{"status":"false","code":"500","reason":"Recieved empty response from the service"}})
                #Response = Response(jsonData,status=200)
                zk.stop()
                return Response(jsonData,200,content_type="application/json")
    else:
        jsonData = jsonify({"result":{"status":"false","code":"500","reason":"Node does not exists"}})
        #resp = Response(jsonData,status=200)
        zk.stop()
        return Response(jsonData,200,content_type="application/json")

@app.route('/acct/balanceget/<ID>',methods=['GET'])
def userBalanceGet(ID):
    zk = KazooClient(hosts=config.ZOOKEEPER_HOST)
    zk.start()
    services = []
    if zk.exists("/microservices/accountservice"):
        data = zk.get("/microservices/accountservice")
        data = json.dumps(data)
        jsonData = json.loads(data)
        Data = jsonData[0]
        JsonData = json.loads(Data)
        balanceURL = str(JsonData["balanceget"]["url"])

        #balanceURL = "http://0.0.0.0:4004/acct/balanceget/"

        try:
            balanceResp = requests.get(balanceURL + ID)
        except HTTPError as http_err:
            jsonData = jsonify({"result":{"status":"false","code":"500","reason":str(http_err)}})
            #resp = Response(jsonData,status=200)
            zk.stop()
            return Response(jsonData,200,content_type="application/json")
        except Exception as err:
            jsonData = jsonifyumps({"result":{"status":"false","code":"500","reason":str(err)}})
            #resp = Response(jsonData,status=200)
            zk.stop()
            return Response(jsonData,200,content_type="application/json")
        else:
            if balanceResp:
                balanceResp = Response(balanceResp,status=200,content_type="application/json")
                zk.stop()
                return balanceResp
            else:
                jsonData = jsonify({"result":{"status":"false","code":"500","reason":"Recieved empty response from the service"}})
                #Response = Response(jsonData,status=200)
                zk.stop()
                return Response(jsonData,200,content_type="application/json")
    else:
        jsonData = jsonify({"result":{"status":"false","code":"500","reason":"Node does not exists"}})
        #resp = Response(jsonData,status=200)
        zk.stop()
        return Response(jsonData,200,content_type="application/json")


if __name__ == '__main__':
    try:
        zk = KazooClient(hosts=config.ZOOKEEPER_HOST,timeout=5,max_retries=3)
        zk.start()
        data = json.dumps({"endpoints":{"url":"http://192.168.200.196:30954"}})
        if zk.exists("/apigateway"):
            zk.set("/apigateway",data)
        else:
            zk.create("/apigateway",data)
    except:
        print('Failed to connect to zookeeper')
        
    
    app.run(debug=config.DEBUG_MODE,host='0.0.0.0',port=config.PORT)