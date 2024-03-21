#!/root/wk/py312/bin/python

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

        self.update_period_value = 1

        self.last_mode = "auto_normal"
        self.vacation_first_date = 0
        self.vacation_second_date = 0

        self.feedback_angle = 0

        self.ch1_vent_status = 0

        self.eco_coef_state = 0
        self.eco_coef_value = 0

    def run(self):
        logger.debug(f"Auto control thread is started")
        self.manage_control_modes()
    

    def manage_control_modes(self):
        while True:
            time.sleep(self.update_period_value)
            curent_date = datetime.date.today()

            current_dt = datetime.datetime.now()
            current_weekday = current_dt.weekday()
            match self.control_mode:
                case "manual":
                    print("Manual mode")
                    self.last_mode = "manual"
                    if self.feedback_angle > 0:
                            self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/VentWidState/on", "blue")
                    else:
                        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/VentWidState/on", "gray")
                case "auto_normal":
                    print("Auto normal mode")
                    self.last_mode = "auto_normal"
                    self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/VentWidState/on", "green")
                    self.set_valve_angle()
                case "auto_week":
                    print("Auto week mode")
                    self.last_mode = "auto_week"
                    self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/VentWidState/on", "green")
                    match current_weekday:
                        case 0 | 1 | 2 | 3 | 4:
                            week_day_start, week_day_end, week_day_current = self.get_unix_timestamps(self.week_start, self.week_stop, current_dt)
                            if week_day_start <= week_day_current <= week_day_end:
                                self.set_valve_angle()
                            else:
                                self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                        case 5 | 6:
                            weeknd_start, weeknd_end, weeknd_current = self.get_unix_timestamps(self.weekend_start, self.weekend_stop, current_dt)
                            if weeknd_start <= weeknd_current <= weeknd_end:
                                self.set_valve_angle()
                            else:
                                self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                        
                case "auto_smart_week":
                    print("Auto smart week mode")
                    self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/VentWidState/on", "green")
                    self.last_mode = "auto_smart_week"
                    period1_start, period1_end, period1_current = self.get_unix_timestamps(self.sw_period1_start, self.sw_period1_stop, current_dt)
                    if period1_start <= period1_current <= period1_end:
                        self.set_valve_angle()
                    else:
                        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                    if self.sw_period2_state:
                        period2_start, period2_end, period2_current = self.get_unix_timestamps(self.sw_period2_start, self.sw_period2_stop, current_dt)
                        if period2_start <= period2_current <= period2_end:
                            self.set_valve_angle()
                        else:
                            self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                    if self.sw_period3_state:
                        period3_start, period3_end, period3_current = self.get_unix_timestamps(self.sw_period3_start, self.sw_period3_stop, current_dt)
                        if period3_start <= period3_current <= period3_end:
                            self.set_valve_angle()
                        else:
                            self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                    if self.sw_period4_state:
                        period4_start, period4_end, period4_current = self.get_unix_timestamps(self.sw_period4_start, self.sw_period4_stop, current_dt)
                        if period4_start <= period4_current <= period4_end:
                            self.set_valve_angle()
                        else:
                            self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                case "vacation":
                    print("Vacation state.")
                    if self.vacation_first_date <= curent_date <= self.vacation_second_date:
                        print("Condition is True. We in vacation range, valve is close")
                        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/VentWidState/on", "gray")
                    else:
                        print("Vacation is end, we will switch to the last control mode")
                        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/ControlMode/on", str(self.last_mode))
                        self.set_mqtt_topic_value(f"/devices/GeneralInfo/controls/VacationState/on", str(0))
                case "alarm":
                    self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(0))
                    self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/VentWidState/on", "red")

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
            case "AirExchangeSet":
                self.air_exchange_value = float(topic_val)
            case "VentPipeDiameter":
                self.vent_pipe_diameter = float(topic_val) / 1000   # milimeters
            case "VentPipeIOHeight":
                self.vent_pipe_io_height = float(topic_val) # meters
            case "VentPipeLength":
                self.vent_pipe_length = float(topic_val)    # meters
            case "28-3c01d075c9e9":
                self.out_temp = float(topic_val)
            case "Temperature1":
                self.home_temp = float(topic_val)
            case "VacationState":
                if int(topic_val):
                    self.control_mode = "vacation"
                else:
                    self.control_mode = self.last_mode
            case "VacationValue1":
                try:
                    self.vacation_first_date = datetime.datetime.strptime(topic_val, '%d.%m.%Y').date()
                except Exception as e:
                    print(e)
            case "VacationValue2":
                try:
                    self.vacation_second_date = datetime.datetime.strptime(topic_val, '%d.%m.%Y').date()
                except Exception as e:
                    print(e)
            case "UpdatePeriod":
                self.update_period_value = int(topic_val)
            case "FeedbackAngle":
                self.feedback_angle = int(topic_val)
            case "VentChannelStatus1":
                self.ch1_vent_status = int(topic_val)
                if self.ch1_vent_status:
                    self.control_mode = "alarm"
                else:
                    self.control_mode = self.last_mode
            case "EcoCoefState":
                self.eco_coef_state = int(topic_val)
            case "EcoCoefValue":
                self.eco_coef_value = int(topic_val)

    def mqtt_start(self):
        client = self.connect_mqtt(f"Ch{self.chan_num} control module")
        self.subscribe(client)
        client.loop_start()


    def set_mqtt_topic_value(self, topic_name: str, value):
        topic = topic_name
        publish.single(topic, str(value), hostname=self.broker)
    
    def set_valve_angle(self):
        print("temparatures: ", f"Home - {self.home_temp}, Out - {self.out_temp}")
        if not self.eco_coef_state:
            air_exch_cval, angle = calculate_angle.calculate_angle(self.vent_pipe_io_height,
                                                           self.vent_pipe_length,
                                                           self.vent_pipe_diameter,
                                                           self.air_exchange_value,
                                                           self.home_temp, self.out_temp)
        else:
            econom_value = (self.eco_coef_value / 100) * self.air_exchange_value
            print("asdsdasdsadasdasdasd", self.eco_coef_value, self.air_exchange_value, econom_value)
            total_air_exchange = self.air_exchange_value - econom_value
            air_exch_cval, angle = calculate_angle.calculate_angle(self.vent_pipe_io_height,
                                                           self.vent_pipe_length,
                                                           self.vent_pipe_diameter,
                                                           total_air_exchange,
                                                           self.home_temp, self.out_temp)
        
        print("Air exchange and angle = ", air_exch_cval, angle)
        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/SetAngle/on", str(angle))
        self.set_mqtt_topic_value(f"/devices/Channel_{self.chan_num}/controls/AirExchangeCalc/on", str(air_exch_cval))
    
    def get_current_hour(self):
        return datetime.datetime.hour

    def get_unix_timestamps(self, start_h, end_h, current_dt):
        current_year = current_dt.year
        current_month = current_dt.month
        current_day = current_dt.day 
        current_hour = current_dt.hour
        if start_h <= end_h:
            start_date_time = datetime.datetime(current_year, current_month, current_day, start_h)
            end_date_time = datetime.datetime(current_year, current_month, current_day, end_h)
            current_date_time = datetime.datetime(current_year, current_month, current_day, current_hour)
        elif start_h > end_h:
            start_date_time = datetime.datetime(current_year, current_month, current_day, start_h)
            end_date_time = datetime.datetime(current_year, current_month, current_day+1, end_h)
            current_date_time = datetime.datetime(current_year, current_month, current_day, current_hour)
        
        start_unix = (time.mktime(start_date_time.timetuple()))
        end_unix = (time.mktime(end_date_time.timetuple()))
        current_unix = (time.mktime(current_date_time.timetuple()))
        return(start_unix, end_unix, current_unix)

def main():
    # broker = "192.168.44.10"
    broker = "localhost"
    port = 1883
    for ch_num in range(1, 3+1):
        channel_control = ChannelControl(mqtt_port=port, mqtt_broker=broker, channel_num=ch_num)
        channel_control.mqtt_start()
        channel_control.start()

if __name__ == "__main__":
    main()
    