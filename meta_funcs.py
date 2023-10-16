 # -*- coding: utf-8 -*-
"""
Module for general functions.
"""

import paho.mqtt.publish as publish


picc_degree_default_dict = {"1": "15", "2": "52", "3": "89",
                            "4": "126", "5": "163", "6": "200"}


def angle_to_dim_level_conv(angle: int) -> float:
    """
    The function converts an angle in degrees to a corresponding voltage value using a conversion
    factor.
    
    :param angle: The angle parameter represents the angle in degrees that you want to convert to
    voltage
    :type angle: int
    :return: the voltage value as a float.
    """
    if isinstance(angle, int):
        k = 10 / 9
        dim_level = k * angle
        return round(dim_level, 2)
    else:
        raise TypeError(f"Type for conversation angle to voltage must be integer, not {type(angle)}!")


def set_angle_position(channel: str, angle: int):
    mqtt_host = "192.168.44.10"
    val = angle_to_dim_level_conv(angle)
    if isinstance(channel, str):
        topic = f"/devices/wb-mao4_26/controls/Channel {channel} Dimming Level/on"
        publish.single(topic, str(val), hostname=mqtt_host)


def voltage_to_angle_conv(value: int) -> str:
    if isinstance(value, int):
        k = 0.009
        angle_value = int(k * value)
        return str(angle_value)
    else:
        raise TypeError(f"Type for conversation angle to voltage must be integer, not {type(value)}!")


def get_degree_pic_id_by_angle(channel: str, angle_val: int):
    picc_id = picc_degree_default_dict[channel]
    match channel:
        case "1":
            if 10 > angle_val >= 0:
                picc_id = "6"
            elif 20 > angle_val >= 10:
                picc_id = "7"
            elif 30 > angle_val >= 20:
                picc_id = "8"
            elif 40 > angle_val >= 30:
                picc_id = "9"
            elif 50 > angle_val >= 40:
                picc_id = "10"
            elif 60 > angle_val >= 50:
                picc_id = "11"
            elif 70 > angle_val >= 60:
                picc_id = "12"
            elif 80 > angle_val >= 70:
                picc_id = "13"
            elif angle_val >= 80:
                picc_id = "14"
        case "2":
            if 10 > angle_val >= 0:
                picc_id = "43"
            elif 20 > angle_val >= 10:
                picc_id = "44"
            elif 30 > angle_val >= 20:
                picc_id = "45"
            elif 40 > angle_val >= 30:
                picc_id = "46"
            elif 50 > angle_val >= 40:
                picc_id = "47"
            elif 60 > angle_val >= 50:
                picc_id = "48"
            elif 70 > angle_val >= 60:
                picc_id = "49"
            elif 80 > angle_val >= 70:
                picc_id = "50"
            elif angle_val >= 80:
                picc_id = "51"
        case "3":
            if 10 > angle_val >= 0:
                picc_id = "80"
            elif 20 > angle_val >= 10:
                picc_id = "81"
            elif 30 > angle_val >= 20:
                picc_id = "82"
            elif 40 > angle_val >= 30:
                picc_id = "83"
            elif 50 > angle_val >= 40:
                picc_id = "84"
            elif 60 > angle_val >= 50:
                picc_id = "85"
            elif 70 > angle_val >= 60:
                picc_id = "86"
            elif 80 > angle_val >= 70:
                picc_id = "87"
            elif angle_val >= 80:
                picc_id = "88"
        case "4":
            if 10 > angle_val >= 0:
                picc_id = "117"
            elif 20 > angle_val >= 10:
                picc_id = "118"
            elif 30 > angle_val >= 20:
                picc_id = "119"
            elif 40 > angle_val >= 30:
                picc_id = "120"
            elif 50 > angle_val >= 40:
                picc_id = "121"
            elif 60 > angle_val >= 50:
                picc_id = "122"
            elif 70 > angle_val >= 60:
                picc_id = "123"
            elif 80 > angle_val >= 70:
                picc_id = "124"
            elif angle_val >= 80:
                picc_id = "125"
    return picc_id


def test():
    # for angle in range(0, 93, 3):
        # res = angle_to_dim_level_conv(angle)
        # print(f"angle {angle} = dim_level {res}")
    
    # angle = 45
    # res = angle_to_dim_level_conv(angle)
    # print(f"angle {angle} = dim_level {res}")
    # set_angle_position("1", angle)

    res = voltage_to_angle_conv(10067)
    print(res)

if __name__ == "__main__":
    test()

