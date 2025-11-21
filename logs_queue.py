import random
import json
from uart_test import get_loc

class ListNode:
    def __init__(self, type=0, freq=None, loc=None):
        self.jamming_type = type
        self.freq = freq
        self.loc = loc
        self.next = None

class Queue:
    def __init__(self, capacity):
        self.head = self.tail = None
        self.capacity = capacity
        self.ct = 0

    def insert(self):
        entry = None
        freq_type = random.randint(0, 3)
        
        if freq_type == 0:
            entry = ListNode(freq_type)
        else:
            # frequency is in MHz
            # type is the waveform type

            # fake latitude and longitude with 7 decimals of accuracy

            frequency = random.uniform(200, 1000)

            lat, long = get_loc()
            location = f'{lat}, {long}'

            entry = ListNode(freq_type, frequency, location)

        if self.ct == self.capacity:
            self.head = self.head.next
            self.ct -= 1

        if not self.head:
            self.head = self.tail = entry
        elif self.head == self.tail:
            self.head.next = entry
            self.tail = entry
        else:
            self.tail.next = entry
            self.tail = self.tail.next

        self.ct += 1


    def get(self):
        if self.head:
            data = self.head
            self.head = self.head.next
            self.ct -= 1

            # (type, frequency, location)
            return json.dumps({'type': data.jamming_type,
                        'frequency': (str(data.freq) + ' MHz' if data.freq else None),
                        'location': data.loc})

        # if the rapsi just started up and has nothing
        return json.dumps({'type': None,
                        'frequency': None,
                        'location': None})


random.seed(12345)