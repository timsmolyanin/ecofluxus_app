from threading import Thread
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import random
import time

from list_of_mqtt_topics import lorawan_sens_parser

from loguru import logger

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")


class ParseLorawanSensors(Thread):
    def __init__(self, mqtt_broker:str, mqtt_port:int, mqtt_user: str, mqtt_passw:str, parent=None):
        super(ParseLorawanSensors, self).__init__(parent)
        self.broker = mqtt_broker
        self.port = mqtt_port
        self.client_id = f"ecofluxus-mqtt-{random.randint(0, 100)}"
        self.comport_open_timeout = 10
        self.mqtt_broker_obj = self.connect_mqtt("BAlbal")

    def run(self):
        """
        The function `run` reads data from a serial port and calls a callback function.
        """
        logger.debug(f"Meow")
        self.mqtt_start()

    def connect_mqtt(self, whois: str) -> mqtt:
        """
        The function `connect_mqtt` connects to an MQTT broker and returns the MQTT client.
        :return: an instance of the MQTT client.
        """
        logger.debug(f"MQTT client in {whois} started connect to broker")
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logger.debug(f"{whois} Connected to MQTT Broker!")
            else:
                logger.debug(f"{whois} Failed to connect, return code {rc}")

        mqtt_client = mqtt.Client(self.client_id)
        mqtt_client.on_connect = on_connect
        mqtt_client.connect(self.broker, self.port)
        return mqtt_client
    

    def subscribe(self, client: mqtt):
        """
        The `subscribe` function subscribes the client to two MQTT topics and sets the `on_message` callback
        function to `self.on_message`.
        
        :param client: The `client` parameter is an instance of the MQTT client that is used to connect to
        the MQTT broker and subscribe to topics
        :type client: mqtt
        """
        try:
            client.subscribe(lorawan_sens_parser) 
            client.on_message = self.on_message
        except Exception as e:
            print(e)
    

    def on_message(self, client, userdata, msg):
        """
        """
        topic_name = msg.topic.split("/")
        topic_val = msg.payload.decode("utf-8")
        dict_data = json.loads(topic_val)
        try:
            object_dict = dict_data.get("object")
            print(object_dict)
            if object_dict:
                tempc = object_dict.get("TempC_SHT")
                print(tempc)
                if tempc:
                    self.set_mqtt_topic_value("/devices/LorawanSensors/controls/Temperature1/on", tempc)
        except:
            print("balbal")
    
    def mqtt_start(self):
        """
        The function `mqtt_start` starts the MQTT client, connects to the MQTT broker, subscribes to
        topics, and starts the client's loop.
        """
        # client = self.connect_mqtt("Nextion MQTT Bridge")
        self.subscribe(self.mqtt_broker_obj)
        self.mqtt_broker_obj.loop_forever()


    def set_mqtt_topic_value(self, topic_name: str, value):
        """
        The function sets the value of a specified MQTT topic.
        
        :param topic_name: A string representing the name of the MQTT topic where the value will be
        published
        :type topic_name: str
        :param value: The value parameter is an integer that represents the value you want to publish to
        the MQTT topic
        :type value: int
        """
        topic = topic_name
        publish.single(topic, str(value), hostname=self.broker)
    

def test():
    broker = "192.168.44.10"
    port = 1883
    get_temperature = ParseLorawanSensors(mqtt_port=port, mqtt_broker=broker, mqtt_passw=None, mqtt_user=None,)
    get_temperature.start()


if __name__ == "__main__":
    test()
    