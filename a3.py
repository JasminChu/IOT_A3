import serial
import time
import paho.mqtt.client as mqtt
import json

from twilio.rest import Client
from beebotte import *

# PERSONAL TESTING api key and secret key
# API_KEY_AUTOLIGHT = 'gTYdN2z6boA2abUcyBjwodf1'
#SECRET_KEY_AUTOLIGHT = 'DvkUcfpV3fikrkowpjJaaVubOrQpXjor'

# GROUP api key and secret key
API_KEY_AUTOLIGHT = 'MNdVZntUkkrD4ONHPw070RKX'
SECRET_KEY_AUTOLIGHT = '7aRoJUz4hOyrdzojpYhe3WPJcYOQFVEE'

#Twilio SMS REST Information
account_sid = "ACdf1050604f3971f8fb2e9b8fa02bc924"
auth_token = "355c59fa5b02a66e5c11305d3f40e10d"

# Setting the resources
bbt = BBT(API_KEY_AUTOLIGHT, SECRET_KEY_AUTOLIGHT)
light_resourse = Resource(bbt, 'Smart_Lighting_System', 'light_intensity_value')
light_button = Resource(bbt, 'Smart_Lighting_System', 'light_onoff')
light_input = Resource(bbt, 'Smart_Lighting_System', 'light_input')
light_auto_onoff = Resource(bbt, 'Smart_Lighting_System', 'light_auto_onoff')
temp_resourse = Resource(bbt, 'Smart_Lighting_System', 'temp_value')
temp_input = Resource(bbt, 'Smart_Lighting_System', 'temp_input')
ser = serial.Serial('/dev/ttyACM0', 9600)

def on_connect(client, data, flags, rc):
    client.subscribe("Smart_Lighting_System/light_intensity_value")
    client.subscribe("Smart_Lighting_System/light_onoff")
    client.subscribe("Smart_Lighting_System/light_input")
    client.subscribe("Smart_Lighting_System/light_auto_onoff")

    client.subscribe("Smart_Lighting_System/temp_value")
    client.subscribe("Smart_Lighting_System/temp_input")


def on_message(client, data, msg):
    
    count=0

    print(msg.topic + " " + str(msg.payload))
    read_light_auto_button_onoff = light_auto_onoff.read(limit=1)
    if (read_light_auto_button_onoff[0]['data']==False):
        read_light_button_onoff = light_button.read(limit=1)
        if(read_light_button_onoff[0]['data'] == True):
            ser.write(b"1")
            print("Manual On")
        elif(read_light_button_onoff[0]['data'] == False):
            ser.write(b"2")
            print("Manual Off")
        else:
            print("No Match")
        time.sleep(5)
        
    elif(read_light_auto_button_onoff[0]['data']==True):
        read_light_input = light_input.read(limit=1)
        read_light_resourse = light_resourse.read(limit=1)
        
        read_temp_input = temp_input.read(limit=1)
        read_temp_resourse = temp_resourse.read(limit=1)

        if(read_light_resourse[0]['data'] <= read_light_input[0]['data'] and read_temp_resourse[0]['data'] <= read_temp_input[0]['data']):
            ser.write(b"1")
            
            count+=1
            if(count==1):
                # SMS script
                smsclient = Client(account_sid, auth_token)
                mailbody = ("We detect the light is on")
                message = smsclient.messages.create(body=mailbody, from_ = "+12018905970",
                to = "+601110679126")
                
            print("Auto On")
            
        elif(read_light_resourse[0]['data'] >read_light_input[0]['data'] and read_temp_resourse[0]['data'] >read_temp_input[0]['data']):
            ser.write(b"2")
            count=0
            print("Auto Off")
        else:
            print("No Match")
        time.sleep(5)
    else:
        print(read_light_auto_button_onoff[0]['data'])
    

# Setup MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# PERSONAL TESTING token
#client.username_pw_set("token:token_WbenCRZsqINb08va")

# GROUP token
client.username_pw_set("token:token_CmG3yJSa0ZaiaPKs")
client.connect("mqtt.beebotte.com", 1883, 60)

client.loop_start()

while True:
    if ser.in_waiting > 0:
        
        ln = ser.readline()
        #light=int(ln);
        #temp=int(ln);
        
        # Reading data
        light=int(ln[23:27])
        temp=int(ln[28:32])
        #print(light)
        #print(temp)
        
        light_dictionary={"data":light,"write":True}
        temp_dictionary={"data":temp,"write":True}
            
        light_json = json.dumps(light_dictionary)
        temp_json = json.dumps(temp_dictionary)
        
        client.publish("Smart_Lighting_System/light_intensity_value", light_json)
        client.publish("Smart_Lighting_System/temp_value", temp_json)
