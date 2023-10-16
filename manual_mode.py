 # -*- coding: utf-8 -*-
"""
Module for manual operation mode.
"""

import meta_funcs
import sqlite_db_skript


def manual_set_angle(channel: str, value: str):
    ctrl_mode = sqlite_db_skript.get_data(ch=channel, variable="ControlMode")
    match ctrl_mode:
        case "manual":
            print(type(value), value)
            meta_funcs.set_angle_position(channel, int(value))


