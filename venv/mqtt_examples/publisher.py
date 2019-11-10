import json
import paho.mqtt.client as mqtt
import time

broker = "localhost"
port = 1883
Connected = False

#with open("msg.json", "r") as read_file:
#    data = json.load(read_file)
    
#for data_id, data_info in data.items():
#    print("\nData ID:", data_id)
    
#    for key in data_info:
#    	print('\n\n')
#        print(key + ':', data_info[key])
 
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")
 
#user = "yourUser"
#password = "yourPassword"
 
client = mqtt.Client("Publisher")               #create new instance
#client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect                      #attach function to callback
client.connect(broker, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.5)
 
try:
    while True:
        value = raw_input('Enter the message:')
        if value == '3':
        	print("ukucao 3")
        client.publish("python/test", value)
        #client.publish("up/data", value)
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()

