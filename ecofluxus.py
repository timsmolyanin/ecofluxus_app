import ch_control
import lorawan_sensors_parser
import alarm_service

def main():
    broker = "192.168.44.10"
    # broker = "192.168.4.15"
    port = 1883

    get_temperature = lorawan_sensors_parser.LorawanSensorsParser(mqtt_port=port, mqtt_broker=broker, mqtt_passw=None, mqtt_user=None,)
    get_temperature.start()

    channel_control = ch_control.ChannelControl(mqtt_port=port, mqtt_broker=broker, channel_num=1)
    channel_control.mqtt_start()
    channel_control.start()

    alarm_ser = alarm_service.AlarmService(mqtt_port=port, mqtt_broker=broker)
    alarm_ser.mqtt_start()
    alarm_ser.start()


if __name__ == "__main__":
    main()