import paho.mqtt.client as mqtt
import time
import json
import psutil
import string
import requests
import time

url = "https://api.thingspeak.com/update.json"
api_key =  "VWXTFZR195SF4BCQ"
digitraffic = "rata-mqtt.digitraffic.fi"

def on_connect(client, userdata, flags, rc):		
	print(f"Connected {rc}")
	client.subscribe("trains/#")		
	
def on_message(client, userdata, msg):
    delay = json.dumps(msg.payload.decode())
    delay = delay.split(",")
    myöhässä = delay[22]
    myöhässä = myöhässä.split(":")
    cancelled = delay[5]
    topic = json.dumps(msg.topic)
    topic = topic.split("/")
    if "Long-distance" in cancelled:
        try:
            aika = int(myöhässä[1])
            print(f"Junan numero: {topic[2]}")
            print(f"Juna Myöhässä: {aika}min")
            print("")
            #payload = {"api_key": api_key, "field2": (str(aika)), "field1": (str(topic[2]))}
            #response = requests.post(url, data=payload)
            tiedosto = {}
            tiedosto['train_number'] = str(topic[2])
            tiedosto['delay_minutes'] = str(aika)
            data = json.loads(json.dumps(tiedosto))
            response = requests.post('http://juna.azurewebsites.net/upload', data=data)
            #client.publish('Delay', payload=str(aika), qos=0, retain=False)
            print(f"send {aika} to myöhässä ")			
            client.connect(digitraffic, 1883, 60)
            if response.status_code == 200:
                print("onnistui")
            else:
                print("ei toimi")
            time.sleep(5)
        except:
            return
    else:
        return
	
def main():
	client = mqtt.Client()				
	client.on_connect = on_connect			
	client.on_message = on_message	
	client.will_set('Delay', b'{"status": "Off"}')
	client.connect("rata-mqtt.digitraffic.fi", 1883, 60)
	client.loop_forever()
        
if __name__ == "__main__":
    main()