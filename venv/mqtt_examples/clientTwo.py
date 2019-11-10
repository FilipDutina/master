import paho.mqtt.client as mqtt

port = 1883

message = ""

def on_connect(client, userdata, flags, rc):
  	print("Connected with result code " + str(rc))
  	#client.subscribe("python/test")
  	client.subscribe("$share/group_one/up/+")

def on_message(client, userdata, msg):
    print("message received ", str(msg.payload.decode("utf-8")))
    print("message topic=", msg.topic)
    print("message qos=", msg.qos)
    print("message retain flag=", msg.retain)
    message = str(msg.payload.decode("utf-8"))
    
client = mqtt.Client("ClientTwo")

client.connect("localhost", port)

client.on_connect = on_connect
client.on_message = on_message

try:
#	client.publish("python/test", message);
	client.loop_forever()
except KeyboardInterrupt:
	client.disconnect()
	client.loop_stop()


