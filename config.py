from os import environ as env
import multiprocessing

PORT = int(env.get("PORT", 4001))
DEBUG_MODE = int(env.get("DEBUG_MODE", 0))
ZOOKEEPER_HOST = "192.168.200.182:2181"
