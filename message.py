import numpy as np

class Message:
    def __init__(self, head, tail, width, length, send_time, travel_time, link):
        self.head = head
        self.tail = tail
        self.width = width
        self.length = length
        self.send_time = send_time
        self.travel_time = travel_time
        self.link = link
        self.time = send_time + travel_time
    
