# Create Device TEST

import os
from src.classes.cl_device import Device

VAR_TEST = "C:\\Users\\g.tronche\\Documents\\test_app"

device = Device(
    device_ipv4="192.168.90.100",
    mask_ipv4="255.255.255.0",
    save_path=VAR_TEST
)

device.save_file()

device.update_auto()

