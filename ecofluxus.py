import ch_control
import get_lorawan_tempearure
import alarm_service

def main():
    broker = "192.168.44.10"
    # broker = "192.168.4.15"
    port = 1883

    get_temperature = get_lorawan_tempearure.ParseLorawanSensors(mqtt_port=port, mqtt_broker=broker, mqtt_passw=None, mqtt_user=None,)
    get_temperature.start()

    channel_control = ch_control.ChannelControl(mqtt_port=port, mqtt_broker=broker)
    channel_control.mqtt_start()
    channel_control.start()

        
if __name__ == "__main__":
    main()