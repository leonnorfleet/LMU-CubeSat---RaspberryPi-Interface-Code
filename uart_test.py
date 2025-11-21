#!/usr/bin/env python

import serial
import time
from pynmeagps import NMEAReader, latlon2dms, latlon2dmm

port = serial.Serial('/dev/serial0', timeout=1)

def get_loc():
    while True:
        # read data
        nmr = NMEAReader(port)
        raw_data, parsed_data = nmr.read()
        if parsed_data is not None and parsed_data.msgID == 'GLL':
                return parsed_data.lat, parsed_data.lon
