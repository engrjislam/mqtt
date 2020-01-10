
# MQTT Client demo
# Continuously monitor different MQTT topics for data,
# check if the received data matches predefined 'commands'
# skip default values
 
import paho.mqtt.client as mqtt
import time


# ---------------------- broker/server ---------------------- #
# broker_host = "192.168.1.184"
# broker_host = "iot.eclipse.org"
broker_host = "test.mosquitto.org"
# default mqtt client port 1883 (insecure) and 8883 (secure)
broker_port = 1883 
# default mqtt keepalive is 60
broker_keepalive = 60 
bind_address=""

# ----------------------- client info ----------------------- #
client_id = 'house-bulbs-on-off'
# default mqtt clean_session is Flase
clean_session = True
protocol = mqtt.MQTTv311 
transport = "tcp"

# ----------------------- topics/urls ----------------------- #
# default mqtt qos is 0
qos = 0 
topic_bulbs = "house/bulbs"
topic_bulb1 = topic_bulbs + "/bulb1"
topic_bulb2 = topic_bulbs + "/bulb2"
topic_bulb3 = topic_bulbs + "/bulb3"
topic_bulb4 = topic_bulbs + "/bulb4"


# ------------------- callback functions -------------------- #
# when the client got any change 
def on_log(client, userdata, level, buf):
    local_time = time.localtime()
    formatted_local_time = time.strftime("%d/%m/%Y %H:%M:%S", local_time)
    # print log in dd/mm/yyyy hh:mm:ss 
    print formatted_local_time, buf

# when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print "Connected with result code "+str(rc)
 
    # subscribe for the topic/urls
    # client.subscribe(topic_bulb1, qos)
    client.subscribe(topic_bulb1)
    client.subscribe((topic_bulb2, qos))
    client.subscribe([(topic_bulb3, qos), (topic_bulb4, qos)])
    # client.subscribe([topic_bulb2, topic_bulb3])
 
# when a PUBLISH message is received from the server.
def on_message(client, userdata, message):
    print "New message received: "
    print "  topic =", message.topic
    print "  qos =", message.qos
    # print "  payload=", str(message.payload.decode("utf-8"))
    print "  payload =", str(message.payload)
    print "  retain =", message.retain
    print "--------------------------------------------------"

    if message.payload.lower() == "on":
        # turn on the light
        pass

# this function usually called after on_connect 
def on_subscribe(client, userdata, mid, granted_qos):
    print "Subscribing the given topics/urls ..."
    # to do list
    pass

# this function usually called after on_connect
def on_unsubscribe(client, userdata, mid):
    print "Unsubscribing the given topics/urls ..."
    # to do list 
    pass

# this function usually called after on_connect
def on_disconnect(client, userdata, rc):
    print "Disconnecting ..."

    # unsubscribe for the topic/urls
    client.unsubscribe(topic_bulb1)
    client.unsubscribe(topic_bulb2)
    client.unsubscribe(topic_bulb3)
    client.unsubscribe(topic_bulb4)

    print "Disconnected with result code " + str(rc)


# --------------- start execution from here --------------- #
if __name__ == '__main__':

    try:
        # Create an MQTT client and attach our routines to it.
        # client = mqtt.Client(client_id, clean_session)
        client = mqtt.Client(client_id, clean_session)

        client.on_log = on_log
        client.on_connect = on_connect
        # client.on_subscribe = on_subscribe
        client.on_message = on_message

        # set username & password
        # client.username_pw_set(username='johirulislam')
        # client.username_pw_set(username='roger', password='password')
     
        # client.connect(broker_host, broker_port, broker_keepalive, bind_address)
        client.connect(broker_host)
     
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
