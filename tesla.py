import paho.mqtt.client as mqtt
import sys
import requests
import time

print("Starting Powerwall App")
sys.stdout.flush()
time.sleep(20)
print("Sleep done...")
sys.stdout.flush()

def on_connect(client, userdata, flags, rc):
    print("ONCONNECT")
    sys.stdout.flush()
    client.loop_start()
    runCommands()


def runCommands():
        print("Making Request to TESLA Battery:")
        sys.stdout.flush()

        r = requests.get('https://192.168.91.1/api/meters/aggregates',verify=False)
        d = r.json()

        print(d)
        print("----")
        sys.stdout.flush()

        batterypwr = d['battery']['instant_power']/1000  #negative means charging
        sitepwr = d['site']['instant_power']/1000    #negative means pushing to grid
        loadpwr = d['load']['instant_power']/1000
        solarpwr = d['solar']['instant_power']/1000

        print("Site "+str(sitepwr))  #GRID
        print("Battery "+str(batterypwr))
        print("Load "+str(loadpwr))
        print("Solar "+str(solarpwr))

        r1 = requests.get('http://192.168.91.1/api/system_status/soe',verify=False)
        d1 = r1.json()
        batterypct = d1['percentage']
        batterycpt = (13500 // (100/batterypct))/1000

        print("Battery PCT "+str(batterypct))
        print("Battery CPT "+str(batterycpt))

        #mqttc.publish("ha/tesla/sitenow",sitepwr)
        client.publish("ha/tesla/loadnow",loadpwr,1)
        client.publish("ha/tesla/batterynow",batterypwr,1)
        client.publish("ha/tesla/gridnow",sitepwr,1)
        client.publish("ha/tesla/solarnow",solarpwr,1)
        client.publish("ha/tesla/batterypct",batterypct,1)
        res = client.publish("ha/tesla/batterycpt",batterycpt,1)
        print (res)

        print("MQTT msgs sent")

        print("Sleeping")
        sys.stdout.flush()





client = mqtt.Client()
#client.on_connect = on_connect
client.connect("pizero1", 1883, 30)
client.loop_start()

while True:
   try: 
    runCommands()
   except: 
    print ("Unexpected error:"+ sys.exc_info()[0])
   time.sleep(10*60)
