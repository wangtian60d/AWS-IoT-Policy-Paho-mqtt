#author: tim wang
# Import package
import paho.mqtt.client as mqtt #activate the virtualenv to have the mqtt package
import ssl
import time
import logging
import json
logging.basicConfig(level=logging.DEBUG)

# Define Variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "$aws/things/shadow/shadow/update"
MQTT_MSG = json.dumps({'state':{'reported':{'color':{'r':255, 'g':255,'b':0}}}})

MQTT_HOST = "a1o2i3ldawkuze.iot.us-east-1.amazonaws.com"
CA_ROOT_CERT_FILE = "./root-CA.crt"
THING_CERT_FILE = "./pahoClient.cert.pem"
THING_PRIVATE_KEY = "./pahoClient.private.key"


# Define on_publish event function
def on_publish(client, userdata, mid):
	print "Message Published... " + str(client) + " " + str(userdata) + " " + str(mid)


# Initiate MQTT Client
mqttc = mqtt.Client("shadow")

logger = logging.getLogger(__name__)
mqttc.enable_logger(logger)
# Register publish callback function
mqttc.on_publish = on_publish

# Configure TLS Set
mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.loop_start()

counter = 0
while True:
	#mqttc.publish(str(counter),MQTT_MSG + str(counter),qos=1)
	mqttc.publish(str(MQTT_TOPIC),MQTT_MSG + str(counter),qos=1)
	counter += 1
	time.sleep(1)

# Disconnect from MQTT_Broker
# mqttc.disconnect()
