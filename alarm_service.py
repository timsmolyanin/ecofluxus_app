from threading import Thread
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import random
import time
import datetime

from list_of_mqtt_topics import alarm_service

from loguru import logger

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")

# /devices/wb-w1/controls/28-3c01d075c9e9/meta/error

class AlarmService(Thread):
    def __init__(self, mqtt_broker:str, mqtt_port:int, parent=None):
        super(AlarmService, self).__init__(parent)
        self.broker = mqtt_broker
        self.port = mqtt_port
        self.client_id = f"ecofluxus-mqtt-{random.randint(0, 100)}"
        self.mqtt_broker_obj = self.connect_mqtt("AlarmService")

        self.alarm_signal_type = "periodic"
        self.alarm_per_min = 5
        self.repeat_alarm_times = 3
        self.alarm_signal_state = 0
        self.alarm_trigger = 0

        self.outdoor_temp_sens_status = 0
        self.vent_channel_status1 = 0

    def run(self):
        while True:
            self.alarm_manager()

    def connect_mqtt(self, whois: str) -> mqtt:
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
        try:
            client.subscribe(alarm_service) 
            client.on_message = self.on_message
        except Exception as e:
            print(e)

    def on_message(self, client, userdata, msg):
        topic_name = msg.topic.split("/")
        topic_val = msg.payload.decode("utf-8")
        print(topic_name, topic_val)
        try:
            match topic_name[-1]:
                case "AlarmSignalType":
                    self.alarm_signal_type = topic_val
                case "AlarmSignalValue":
                    self.set_mqtt_topic_value("/devices/buzzer/controls/volume/on", str(topic_val))
                case "PeriodicAlarmPerMin":
                    self.alarm_per_min = int(topic_val)
                case "RepeatAlarmPerMin":
                    self.alarm_per_min = int(topic_val)
                case "RepeatAlarmTimes":
                    self.repeat_alarm_times = int(topic_val)
                case "AlarmSignalState":
                    self.alarm_signal_state = int(topic_val)
                case "OutdoorTempSensStatus" | "VentChannelStatus1" | "VentChannelStatus2" | "VentChannelStatus3" | "VentChannelStatus4" | "VentChannelStatus5" | "VentChannelStatus6":
                    self.alarm_trigger = int(topic_val)
                    if int(self.alarm_trigger) == 0:
                        self.set_mqtt_topic_value("/devices/wb-gpio/controls/D1_OUT/on", str(0))
                case "error":
                    match topic_name[-3]:
                        case "IN 1 N Voltage":
                            if topic_val == "":
                                self.set_mqtt_topic_value("/devices/AlarmService/controls/VentChannelStatus1/on", str(0))
                            elif topic_val in ("r", "w"):
                                self.set_mqtt_topic_value("/devices/AlarmService/controls/VentChannelStatus1/on", str(1))
                        case "28-3c01d075c9e9":
                            if topic_val == "":
                                self.set_mqtt_topic_value("/devices/AlarmService/controls/OutdoorTempSensStatus/on", str(0))
                            elif topic_val in ("r", "w"):
                                self.set_mqtt_topic_value("/devices/AlarmService/controls/OutdoorTempSensStatus/on", str(1))
        except Exception as err:
            print(err)
    
    def mqtt_start(self):
        self.subscribe(self.mqtt_broker_obj)
        self.mqtt_broker_obj.loop_start()

    def set_mqtt_topic_value(self, topic_name: str, value):
        topic = topic_name
        publish.single(topic, str(value), hostname=self.broker)
    
    def alarm_manager(self):
        while True:
            time.sleep(self.alarm_per_min)
            if self.alarm_signal_state:
                if self.alarm_trigger:
                    self.set_mqtt_topic_value("/devices/wb-gpio/controls/D1_OUT/on", str(1))
                    match self.alarm_signal_type:
                        case "periodic":
                            self.alarm_periodic()
                        case "continuos":
                            self.set_mqtt_topic_value("/devices/buzzer/controls/enabled/on", 1)
                        case "repeatedly":
                            self.alarm_repeatedly()
                else:
                    self.set_mqtt_topic_value("/devices/buzzer/controls/enabled/on", 0)
                    self.set_mqtt_topic_value("/devices/wb-gpio/controls/D1_OUT/on", str(0))
            else:
                self.set_mqtt_topic_value("/devices/buzzer/controls/enabled/on", 0)
                self.set_mqtt_topic_value("/devices/wb-gpio/controls/D1_OUT/on", str(0))

    def alarm_repeatedly(self):
        alarm_state = 0
        times_count = 0
        t1 = 0
        while True:
            if self.alarm_signal_state:
                if alarm_state:
                    self.set_mqtt_topic_value("/devices/buzzer/controls/enabled/on", 0)
                    alarm_state = 0
                    time.sleep(1)
                    t1 += 1
                else:
                    self.set_mqtt_topic_value("/devices/buzzer/controls/enabled/on", 1)
                    alarm_state = 1
                    time.sleep(1)
                    t1 += 1
                if t1 == 2:
                    times_count += 1
                    t1 = 0
                if times_count >= self.repeat_alarm_times:
                    times_count = 0
                    break
    
    def alarm_periodic(self):
        alarm_state = 0
        t1 = 0
        while True:
            if self.alarm_signal_state:
                if alarm_state:
                    self.set_mqtt_topic_value("/devices/buzzer/controls/enabled/on", 0)
                    alarm_state = 0
                    time.sleep(1)
                    t1 += 1
                else:
                    self.set_mqtt_topic_value("/devices/buzzer/controls/enabled/on", 1)
                    alarm_state = 1
                    time.sleep(1)
                    t1 += 1
                if t1 == 2:
                    t1 = 0
                    break


def main():
    broker = "192.168.44.10"
    # broker = "192.168.4.15"
    port = 1883

    alarm_service = AlarmService(mqtt_port=port, mqtt_broker=broker)
    alarm_service.mqtt_start()
    alarm_service.start()


if __name__ == "__main__":
    main()