from threading import Thread
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import random
import time
import datetime
import json

import list_of_mqtt_topics
import calculate_angle

from loguru import logger

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")


# The `NextionMqttBridge` class is a thread that connects to a Nextion display via serial
# communication and bridges it with an MQTT broker.
class ChannelControl(Thread):
    def __init__(self, mqtt_broker:str, mqtt_port:int, parent=None):
        super(ChannelControl, self).__init__(parent)
        self.broker = mqtt_broker
        self.port = mqtt_port
        self.client_id = f"ecofluxus-mqtt-{random.randint(0, 100)}"
        self.comport_open_timeout = 10

        self.control_mode = "manual"

        self.sw_period1_state = 0
        self.sw_period1_start = 0
        self.sw_period1_stop = 0
        self.sw_period2_state = 0
        self.sw_period2_start = 0
        self.sw_period2_stop = 0
        self.sw_period3_state = 0
        self.sw_period3_start = 0
        self.sw_period3_stop = 0
        self.sw_period4_state = 0
        self.sw_period4_start = 0
        self.sw_period4_stop = 0

        self.week_start = 0
        self.week_stop = 0
        self.weekend_start = 0
        self.weekend_stop = 0

        self.vent_pipe_diameter = 0
        self.vent_pipe_io_height = 0
        self.vent_pipe_length = 0
        self.air_exchange_value = 0

        self.out_temp = 0
        self.home_temp = 15

    def run(self):
        """
        The function `run` reads data from a serial port and calls a callback function.
        """
        logger.debug(f"Auto control thread is started")
        self.manage_auto_control_modes()
    

    def manage_auto_control_modes(self):
        while True:
            current_dt = datetime.datetime.now()
            current_weekday = current_dt.weekday()
            current_hour = current_dt.hour
            time.sleep(2)
            match self.control_mode:
                case "manual":
                    pass
                case "auto_normal":
                    print("out = ", self.out_temp, "home = ", self.home_temp)
                    data = calculate_angle.calculate_angle(self.vent_pipe_io_height,
                                                           self.vent_pipe_length,
                                                           self.vent_pipe_diameter,
                                                           self.air_exchange_value,
                                                           30, self.out_temp)
                    print(data)
                case "auto_week":
                    match current_weekday:
                        case 0 | 1 | 2 | 3 | 4:
                            if current_hour in range(self.week_start, self.week_stop):
                                data = calculate_angle.calculate_angle(self.vent_pipe_io_height,
                                                           self.vent_pipe_length,
                                                           self.vent_pipe_diameter,
                                                           self.air_exchange_value,
                                                           25, 15)
                                # print(data)
                        case 5 | 6:
                            if current_hour in range(self.weekend_start, self.weekend_stop):
                                data = calculate_angle.calculate_angle(self.vent_pipe_io_height,
                                                           self.vent_pipe_length,
                                                           self.vent_pipe_diameter,
                                                           self.air_exchange_value,
                                                           25, 15)
                                # print(data)
                case "auto_smart_week":
                    if current_hour in range(self.sw_period1_start, self.sw_period1_stop):
                        data = calculate_angle.calculate_angle(self.vent_pipe_io_height,
                                                           self.vent_pipe_length,
                                                           self.vent_pipe_diameter,
                                                           self.air_exchange_value,
                                                           25, 15)
                        # print(data)
                    if self.sw_period2_state:
                        if current_hour in range(self.sw_period2_start, self.sw_period2_stop):
                            data = calculate_angle.calculate_angle(self.vent_pipe_io_height,
                                                           self.vent_pipe_length,
                                                           self.vent_pipe_diameter,
                                                           self.air_exchange_value,
                                                           25, 15)
                            # print(data)
                    if self.sw_period3_state:
                        if current_hour in range(self.sw_period3_start, self.sw_period3_stop):
                            data = calculate_angle.calculate_angle(self.vent_pipe_io_height,
                                                           self.vent_pipe_length,
                                                           self.vent_pipe_diameter,
                                                           self.air_exchange_value,
                                                           25, 15)
                            # print(data)
                    if self.sw_period4_state:
                        if current_hour in range(self.sw_period4_start, self.sw_period4_stop):
                            data = calculate_angle.calculate_angle(self.vent_pipe_io_height,
                                                           self.vent_pipe_length,
                                                           self.vent_pipe_diameter,
                                                           self.air_exchange_value,
                                                           25, 15)
                            # print(data)


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
            client.subscribe(list_of_mqtt_topics.ch1_topic_list) 
            client.on_message = self.on_message
        except Exception as e:
            print(e)

    def on_message(self, client, userdata, msg):
        """
        """
        topic_name = msg.topic.split("/")
        topic_val = msg.payload.decode("utf-8")
        # print(topic_name, topic_val)
        match topic_name[-1]:
            case "ControlMode":
                self.control_mode = topic_val
            case "WeekStart":
                self.week_start = int(topic_val)
            case "WeekStop":
                self.week_stop = int(topic_val)
            case "WeekendStart":
                self.weekend_start = int(topic_val)
            case "WeekendStop":
                self.weekend_stop = int(topic_val)
            case "SWPeriod1Start":
                self.sw_period1_start = int(topic_val)
            case "SWPeriod1Stop":
                self.sw_period1_stop = int(topic_val)
            case "SWPeriod2State":
                self.sw_period2_state = bool(int(topic_val))
            case "SWPeriod2Start":
                self.sw_period2_start = int(topic_val)
            case "SWPeriod2Stop":
                self.sw_period2_stop = int(topic_val)
            case "SWPeriod3State":
                self.sw_period3_state = bool(int(topic_val))
            case "SWPeriod3Start":
                self.sw_period3_start = int(topic_val)
            case "SWPeriod3Stop":
                self.sw_period3_stop = int(topic_val)
            case "SWPeriod4State":
                self.sw_period4_state = bool(int(topic_val))
            case "SWPeriod4Start":
                self.sw_period4_start = int(topic_val)
            case "SWPeriod4Stop":
                self.sw_period4_stop = int(topic_val)
            case "AirExchangeValue":
                self.air_exchange_value = float(topic_val)
            case "VentPipeDiameter":
                self.vent_pipe_diameter = float(topic_val)
            case "VentPipeIOHeight":
                self.vent_pipe_io_height = float(topic_val)
            case "VentPipeLength":
                self.vent_pipe_length = float(topic_val)
            case "28-3c01d075c9e9":
                self.out_temp = float(topic_val)
                # print(topic_val)
            case "up":
                aDict = json.loads(topic_val)
                try:
                    self.home_temp = float(aDict["object"]["TempC_SHT"])
                except:
                    print("balbal")


    def mqtt_start(self):
        """
        The function `mqtt_start` starts the MQTT client, connects to the MQTT broker, subscribes to
        topics, and starts the client's loop.
        """
        client = self.connect_mqtt("Ch1 auto control")
        self.subscribe(client)
        client.loop_start()


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
    
    def get_current_hour(self):
        return datetime.datetime.hour
    

def test():
    broker = "192.168.44.10"
    # broker = "192.168.4.15"
    port = 1883
    channel_control = ChannelControl(mqtt_port=port, mqtt_broker=broker)
    channel_control.mqtt_start()
    channel_control.start()
    # json_str = '{"deduplicationId":"838f2b6e-a781-48ec-9a79-600442adbe7c","time":"2024-02-29T16:01:18.118252739+00:00","deviceInfo":{"tenantId":"52f14cd4-c6f1-4fbd-8f87-4025e1d49242","tenantName":"ChirpStack","applicationId":"9f1832a7-2862-4e8e-9c20-0f8342e689de","applicationName":"Sensors","deviceProfileId":"f35e1cad-8571-405d-85c3-e4c6b01c4e90","deviceProfileName":"LHT52","deviceName":"LHT52","devEui":"a840415711866a85","deviceClassEnabled":"CLASS_A","tags":{}},"devAddr":"01272c9e","adr":true,"dr":5,"fCnt":1,"fPort":2,"confirmed":false,"data":"CmQCD3//AWXgqk4=","object":{"TempC_SHT":26.6,"Hum_SHT":52.7,"TempC_DS":327.67,"Systimestamp":1709222478.0,"Ext":1.0},"rxInfo":[{"gatewayId":"0016c001f1427f6e","uplinkId":1966232800,"nsTime":"2024-02-29T16:01:17.868407010+00:00","rssi":-49,"snr":14.2,"channel":4,"location":{},"context":"SWed3w==","metadata":{"region_config_id":"eu868","region_common_name":"EU868"},"crcStatus":"CRC_OK"}],"txInfo":{"frequency":867300000,"modulation":{"lora":{"bandwidth":125000,"spreadingFactor":7,"codeRate":"CR_4_5"}}}}'
    # adict = json.loads(json_str)
    # print(adict)
    # print("---")
    # print(adict["object"]["TempC_SHT"])

if __name__ == "__main__":
    test()
    