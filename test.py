import os 
import json
from time import time

datapath = os.path.exists('data.json')

if datapath == False:
    open('data.json', 'x')
    with open('data.json', 'w') as data:
        info = {
            "amazon": {"sent": False, "timestamp": None},
            "bestbuy": {"sent": False, "timestamp": None},
            "target": {"sent": False, "timestamp": None},
            "walmart": {"sent": False, "timestamp": None},
            "gamestop": {"sent": False, "timestamp": None}
        }
        json.dump(info, data)
        print('Data file created.')

with open('data.json') as data:
    global information
    content = data.read()
    information = json.loads(content)
    data.close()
timenow = time()
information['amazon']['sent'] = True
information['amazon']['timestamp'] = timenow
with open('data.json', 'w') as data:
    json.dump(information, data, indent=2)
