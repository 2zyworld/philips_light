

import time

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# Initial the dht device, with data pin connected to:
broker_address="13.212.113.54"  # raspberryPi
broker_port=1883
client = mqtt.Client() #create new instance
print("connecting to broker")
client.connect(host=broker_address, port=broker_port)
print("Subscribing to topic","data/#")

while True:
    try:
        val = "setting,mood,3DFF92,on"
        client.publish("data/light", val)
        

        
    
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        raise error
    except KeyboardInterrupt:
        print("bye")

    time.sleep(1.0)