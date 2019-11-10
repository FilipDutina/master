import paho.mqtt.client as mqtt

port = 1883

message = ""

clients = []
mqtt.Client.connected_flag = False

def on_connect(client, userdata, flags, rc):
  	print("Connected with result code " + str(rc))
  	#client.subscribe("python/test")
  	client.subscribe("$share/group_one/up/+")

def on_message(client, userdata, msg):
	print("client id ", str(client.clientId))
    print("message received ", str(msg.payload.decode("utf-8")))
    print("message topic=", msg.topic)
    print("message qos=", msg.qos)
    print("message retain flag=", msg.retain)
    message = str(msg.payload.decode("utf-8"))
    
for i in range(3):
	cname = "Client"+str(i)
	client = mqtt.Client(cname)
	clients.append(client)
	
for client in clients:
	client.connect("localhost", port)
	client.on_connect = on_connect
	client.on_message = on_message
    
#client = mqtt.Client("ClientOne")

#client.connect("localhost", port)

#client.on_connect = on_connect
#client.on_message = on_message

try:
#	client.publish("python/test", message);
	for client in clients:
		client.loop_forever()
except KeyboardInterrupt:
	client.disconnect()
	client.loop_stop()
