import paho.mqtt.client as mqtt #import the client1
import time


# broker_address="192.168.1.184"
# broker_address="iot.eclipse.org"
# broker_address = "test.mosquitto.org"
broker_address = "192.168.0.52"
broker_port = 1883
broker_keepalive = 60

topic_bulbs = "house/bulbs"
topic_bulb1 = topic_bulbs + "/bulb1"
topic_bulb2 = topic_bulbs + "/bulb2"
topic_bulb3 = topic_bulbs + "/bulb3"


########################################
def on_log(client, userdata, level, buf):
    local_time = time.localtime()
    formatted_local_time = time.strftime("%d/%m/%Y %H:%M:%S", local_time)
    print formatted_local_time, buf

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic_bulb1)
    client.subscribe(topic_bulb2)
    client.subscribe(topic_bulb3)

def on_subscribe(client, userdata, mid, granted_qos):
	# pass
	print("Subscribing ... ")

def on_unsubscribe(client, userdata, mid):
	# pass
	print("Unsubscribing ... ")

def on_message(client, userdata, message):
    print "New message received: "
    print "  topic =", message.topic
    print "  qos =", message.qos
    print "  payload =", str(message.payload.decode("utf-8"))
    print "  retain =", message.retain
    print "--------------------------------------------------"

def on_disconnect(client, userdata, rc):
    print("Disconnecting ...")

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.unsubscribe(topic_bulb1)

    print("Disconnected with result code " + str(rc))
########################################



if __name__ == '__main__':

    try:
        # Create an MQTT client and attach our routines to it.
        client = mqtt.Client("house")
        client.on_log = on_log
        client.on_connect = on_connect
        # client.on_subscribe = on_subscribe
        client.on_message = on_message
     
        client.connect(broker_address, broker_port, broker_keepalive)
     
        # Process network traffic and dispatch callbacks. This will also handle
        # reconnecting. Check the documentation at
        # https://github.com/eclipse/paho.mqtt.python
        # for information on how to use other loop*() functions
        client.loop_forever()
    except KeyboardInterrupt:
        # disconnect
        # client.on_unsubscribe = on_unsubscribe
        # client.on_disconnect = on_disconnect
        client.disconnect() 