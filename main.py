#!/root/wk/py310/bin/python

import serial_port
import nextion_mqtt_bridge
import paho.mqtt.client as mqtt
import yaml


def main():
    serial_com_port_name = "COM5"
    serial_com_port_speed = 115200
    mqtt_broker_address = "192.168.44.10"
    mqtt_broker_port = 1883

if __name__ == "__main__":
    main()
