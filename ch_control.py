from threading import Thread
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import random
import time
import datetime

import list_of_mqtt_topics

from loguru import logger

import calculate_angle

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG")


class ChannelControl(Thread):
    def __init__(self, mqtt_broker:str, mqtt_port:int, channel_num:int, parent=None):
        super(ChannelControl, self).__init__(parent)
        self.broker = mqtt_broker
        self.port = mqtt_port
        self.client_id = f"ecofluxus-mqtt-{random.randint(0, 100)}"
        self.comport_open_timeout = 10

        self.chan_num = channel_num
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
        self.home_temp = 0

        self.update_period_value = 60

        self.last_mode = ""
        self.vacation_first_date = 0
        self.vacation_second_date = 0

    def run(self):
        logger.debug(f"Auto control thread is started")
        self.manage_control_modes()
    

    def manage_auto_control_modes(self):
        while True:
            time.sleep(self.update_period_value)
            current_dt = datetime.datetime.now()
            current_weekday = current_dt.weekday()
            current_hour = current_dt.hour
            match self.control_mode:
                case "manual":
                    self.last_mode = "manual"
                    pass
                case "auto_normal":
                    self.last_mode = "auto_normal"
                    self.set_valve_angle()
                case "auto_week":
                    self.last_mode = "auto_week"
                    match current_weekday:
                        case 0 | 1 | 2 | 3 | 4:
                            if current_hour in range(self.week_start, self.week_stop):
                                self.set_valve_angle()
                            else:
                                self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                        case 5 | 6:
                            if current_hour in range(self.weekend_start, self.weekend_stop):
                                self.set_valve_angle()
                            else:
                                self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                case "auto_smart_week":
                    self.last_mode = "auto_smart_week"
                    if current_hour in range(self.sw_period1_start, self.sw_period1_stop):
                        self.set_valve_angle()
                    else:
                        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                    if self.sw_period2_state:
                        if current_hour in range(self.sw_period2_start, self.sw_period2_stop):
                            self.set_valve_angle()
                        else:
                            self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                    if self.sw_period3_state:
                        if current_hour in range(self.sw_period3_start, self.sw_period3_stop):
                            self.set_valve_angle()
                        else:
                            self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                    if self.sw_period4_state:
                        if current_hour in range(self.sw_period4_start, self.sw_period4_stop):
                            self.set_valve_angle()
                        else:
                            self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                case "vacation":
                    if current_hour in range(self.vacation_first_date, self.vacation_second_date):
                        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                    else:
                        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/ControlMode/on", str(self.last_mode))


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
            case "Temperature1":
                self.home_temp = float(topic_val)


    def mqtt_start(self):
        client = self.connect_mqtt(f"Ch{self.chan_num} control module")
        self.subscribe(client)
        client.loop_start()


    def set_mqtt_topic_value(self, topic_name: str, value):
        topic = topic_name
        publish.single(topic, str(value), hostname=self.broker)
    
    def set_valve_angle(self):
        air_exch_cval, angle = calculate_angle.calculate_angle(self.vent_pipe_io_height,
                                                           self.vent_pipe_length,
                                                           self.vent_pipe_diameter,
                                                           self.air_exchange_value,
                                                           self.home_temp, self.out_temp)
        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(angle))
        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/AirExchangeCalc/on", str(air_exch_cval))
    
    def get_current_hour(self):
        return datetime.datetime.hour
    

def test():
    broker = "192.168.44.10"
    # broker = "192.168.4.15"
    port = 1883
    channel_control = ChannelControl(mqtt_port=port, mqtt_broker=broker, channel_num=1)
    channel_control.mqtt_start()
    channel_control.start()

if __name__ == "__main__":
    test()
    