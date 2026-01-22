#!/usr/bin/env python

import time
import pigpio
from logs_queue import *
from uart_test import port

I2C_ADDR=0x13

QUEUE_SIZE = 10
logs = Queue(QUEUE_SIZE)

pi = pigpio.pi()

if not pi.connected:
    exit()

'''
if the aardvark randomly breaks just unplug everything and check the pins
'''

def i2c(id, tick):
    global pi

    s, b, d = pi.bsc_i2c(I2C_ADDR)

    if b:
        print('received:', d[:].decode('utf-8'))

        if d[0] == ord('R'):
            # bsc_i2c can only store a max of 16 bytes

            msg = logs.get()
            pi.bsc_i2c(I2C_ADDR, '12345678123456781234567812345678')          


def b_i2c():
    # Respond to BSC target activity

    e = pi.event_callback(pigpio.EVENT_BSC, i2c)

    pi.bsc_i2c(I2C_ADDR) # Configure BSC as I2C target

    try:
        print('Listening on address 0x13 as I2C target..')
        while True:
            logs.insert()
            time.sleep(0.5)

    except KeyboardInterrupt:
        e.cancel()
        pi.bsc_i2c(0) # Disable BSC peripheral
        pi.stop()


def b_xfer():
    BSC_I2C_MODE = 1 << 8
    BSC_ENABLE   = 1

    bsc_control = (I2C_ADDR << 16) | BSC_I2C_MODE | BSC_ENABLE | (1 << 3) | (1 << 2)
    pi.bsc_xfer(bsc_control, b'')

    msg = b''
    chunk_size = 16
    

    print('Listening on address 0x13 as I2C target..')

    try:
        t = time.time()
        while True:
            if time.time() - t >= 1:
                logs.insert()
                t = time.time()

            s, c, d = pi.bsc_xfer(bsc_control, b'')

            if c > 0:
                '''
                ##### TRANSCEIVER I2C MESSAGE FORMAT #####
                ES+W22FB + length of log data + log data + ' ' + CRC32/ISO-HDLC
                '''

                recv = d.decode(errors='ignore')
                print('received:', recv)

                if recv and recv[0] == 'R':
                    if not msg:
                        log_data = (logs.get() + '|').encode('utf-8')
                        print(log_data)
                        msg = log_data + b'\0'

                    tx = msg[:chunk_size]
                    msg = msg[chunk_size:]

                    if not tx:
                        tx = b'\0' * chunk_size

                    # Make sure tx is exactly chunk_size
                    if len(tx) < chunk_size:
                        tx += b'\0' * (chunk_size - len(tx))

                    pi.bsc_xfer(bsc_control, tx)

            time.sleep(0.02)

    except KeyboardInterrupt:
        pi.bsc_xfer(0, b'')
        pi.stop()
        port.close()


b_xfer()