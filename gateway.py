from flask import Flask
from flask import jsonify
from flask import request
from kazoo.client import KazooClient
import json
import requests
import random
from requests.exceptions import HTTPError
import config
import logging

logging.basicConfig()

app = Flask(__name__)

@app.route('/auth/health',methods=['GET'])
def healthResponse():
    if zoo_healthCheck() == True:
        resp = jsonify(success=True)
        resp.status_code = 200
        return resp
    else:
        resp = jsonify(success=False)
        resp.status_code = 500
        return resp

def zoo_healthCheck():
    try:
        zk = KazooClient(hosts=config.ZOOKEEPER_HOST)
        zk.start()
        return True
    except:
        print("Cannot connect to zookeeper")
        return False

@app.route('/auth/validate/<userName>/<password>',methods=['POST'])
def userValidate(userName,password):
    zk = KazooClient(hosts=config.ZOOKEEPER_HOST)
    zk.start()
    services = []
    if zk.exists("/microservices"):
        # print(zk.get_children("/jarvis"))
        for service in zk.get_children("/microservices"):
            data,stat = zk.get("/microservices/" + str(service))
            # print(str(service) + " Data : " + data.decode('utf-8'))
            jsonData = json.loads(data.decode('utf-8'))
            healthURL = jsonData["healthcheck"]["url"]
            try:
                healthData = requests.get(str(healthURL),timeout=1)
                healthData.raise_for_status()
            except HTTPError as http_err:
                print('HTTP error occurred:') 
            except Exception as err:
                print('Other error occurred')
            else:
                if healthData:
                    jsonhealthData = healthData.json()["result"]
                    # print(str(service) + " : " + " Memory : " + jsonhealthData["memPercent"] + " CPU : " + jsonhealthData["cpuPercent"] + " Disk : " + jsonhealthData["diskPercent"])
                    if float(jsonhealthData["memPercent"])<80.0 and float(jsonhealthData["cpuPercent"])<50.0 and float(jsonhealthData["diskPercent"])<20.0 :
                        services.append(jsonData["authservice"]["url"])
    zk.stop()
    if len(services)>0:
        pServiceURL = str(random.choice(services))
        pServiceURL = pServiceURL + userName + "/" + password
        print("Picked  : " + pServiceURL)
        return requests.post(pServiceURL).json()
    else:
        result = json.dumps({"result":{"Error":"No Service Found"}})
        print(result)
        return result

if __name__ == '__main__':
    app.run(debug=config.DEBUG_MODE,host='0.0.0.0',port=config.PORT)