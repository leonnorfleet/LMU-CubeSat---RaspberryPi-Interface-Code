#!/usr/bin/env python

import serial
import time
from pynmeagps import NMEAReader, latlon2dms, latlon2dmm

port = serial.Serial('/dev/serial0', timeout=1)

nmr = NMEAReader(port)

def get_loc():
    while True:
        # read data
        raw_data, parsed_data = nmr.read()

        try:
            if parsed_data is not None and parsed_data.msgID == 'GLL':
                return parsed_data.lat, parsed_data.lon
            # else:
            #     # print('GPS module not calibrated yet')
            #     return None, None
        except Exception as e:
            # print(e)
            return None, None
