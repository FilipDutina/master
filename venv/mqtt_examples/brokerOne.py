import paho.mqtt.client as mqtt
import time

port = 1883

message = ""
sent = False

def on_connect(client, userdata, flags, rc):
  	print("Connected with result code " + str(rc))
  	client.subscribe("python/test")
  	#client.subscribe("$share/group_one/up/+")

def on_message(client, userdata, msg):
    print("message received ", str(msg.payload.decode("utf-8")))
    print("message topic=", msg.topic)
    print("message qos=", msg.qos)
    print("message retain flag=", msg.retain)
    message = str(msg.payload.decode("utf-8"))
    client.publish("up/data", message)
    
client = mqtt.Client("BrokerOne")

client.on_connect = on_connect
client.connect("localhost", port)
client.on_message = on_message
#client.loop_start()

try:
	client.loop_forever()
except KeyboardInterrupt:
	client.disconnect()
	client.loop_stop()


