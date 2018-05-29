import sys
sys.path.append('..')
from drm_api import Client, Api
import json


def get_env():
    with (open("environment.json", "r")) as fp:
        data = fp.read()
        out = json.loads(data)
        return out


env = get_env()
client = Client(web_service=env["local"]["web"], drm_adapter=Api(env["local"]["drm"]))
resp = client.get_node_types()
print(resp.content)