from cmath import inf
import numpy as np

class Link():
    def __init__(self, id, head, tail):
        self.id = id
        self.head = head
        self.tail = tail
        self.last_arrived = 0
        self.length = inf
        self.width = 0
    
    def update(self, time):
        self.last_arrived = max(self.last_arrived, time)

    def nullify(self):
        self.last_arrived = 0
