
from multiprocessing import parent_process 


# -*- coding: utf-8 -*- 
#---- subscriber.py  데이터 받기 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish



from phue import Bridge
import time
import logging
from rgbxy import Converter

light_val = [0,0,0,0]
message_val = [0,0]

state_1 = 0
state_2 = 0
color = [0,]
recommend_color = "FFFFFF"
rec_color = [0,0,0]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

#서버로부터 publish message를 받을 때 호출되는 콜백
def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))
    
def on_message(client, userdata, msg):

    
    global light_val
    global message
    global color
    global recommend_color
    global rec_color
    

    print(str(msg.payload.decode("utf-8")))
    message = str(msg.payload.decode("utf-8"))
    print(message)
 
    
    light_val = message.split(",")
    print(light_val)

    if(light_val[0]=="color"):
        recommend_color = light_val[1]
        rec_color = converter.hex_to_xy(f"{recommend_color}")
        print(rec_color)
        
    elif((light_val[0]=="init")|(light_val[0]=="init_return")):
        nw_light_val = light_val[2]
        if(nw_light_val[0] == "#"):
            light_val[2] = nw_light_val[1:]
        hex_color = f"{light_val[2]}"
        color = converter.hex_to_xy(f"{hex_color}")

    
        
    
    


    

    
    

    
try:
    client = mqtt.Client() #client 오브젝트 생성
    client.on_connect = on_connect #콜백설정
    client.on_subscribe = on_subscribe
    client.on_message = on_message #콜백설정

    client.connect('172.30.1.52', 1883)  # 라즈베리파이 커넥트  
    # client.connect('localhost', 1883)  # 라즈베리파이 커넥트  
    client.subscribe('Iot/light', 0)  # 토픽 : temp/temp  | qos : 1
    client.publish('data',"init,mood")
    client.loop_start()

    logging.basicConfig()
    converter = Converter()
   

    b = Bridge('172.30.1.9') 
    # b.connect()

    while True:
        if(light_val[0] == "recommend"):
            b.set_light(1, 'on', True)
            b.set_light(1, 'xy', [rec_color[0],rec_color[1]])
            recommend_color = 0
        elif((light_val[0]=="init")|(light_val[0]=="init_return")):
            if(light_val[3] == 'on'):
                state_1 += 1
                if(state_1 == 1):
                    b.set_light(1, 'on', True)
                    b.set_light(1, 'xy', [color[0],color[1]])
                    state_1 = 0
            if(light_val[3] == 'off'):
                state_2 += 1
                if(state_2 == 1):
                    b.set_light(1, 'on', False)
                    state_2 = 0
        
        





    

except KeyboardInterrupt:
    print("bye")