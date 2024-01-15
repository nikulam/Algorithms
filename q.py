class MessageQueue():
    def __init__(self):
        self.queue = []

    def isEmpty(self):
        return len(self.queue) == 0
 
    def insert(self, data):
        self.queue.append(data)
 
    def pop(self):
        max = 0
        for i in range(len(self.queue)):
            if self.queue[i].time < self.queue[max].time:
                max = i
        item = self.queue[max]
        del self.queue[max]
        return item


class ShortestQueue():
    def __init__(self):
        self.queue = []

    def isEmpty(self):
        return len(self.queue) == 0
 
    def insert(self, data):
        self.queue.append(data)
 
    def pop(self):
        max = 0
        for i in range(len(self.queue)):
            if self.queue[i].wsp['length'] < self.queue[max].wsp['length']:
                max = i
            elif self.queue[i].wsp['length'] == self.queue[max].wsp['length'] and self.queue[i].wsp['width'] > self.queue[max].wsp['width']:
                max = i
        item = self.queue[max]
        del self.queue[max]
        return item

class WidestQueue():
    def __init__(self):
        self.queue = []

    def isEmpty(self):
        return len(self.queue) == 0
 
    def insert(self, data):
        self.queue.append(data)
 
    def pop(self):
        max = 0
        for i in range(len(self.queue)):
            if self.queue[i].naive_swp['width'] > self.queue[max].naive_swp['width']:
                max = i
            elif self.queue[i].naive_swp['width'] == self.queue[max].naive_swp['width'] and self.queue[i].naive_swp['length'] < self.queue[max].naive_swp['length']:
                max = i
        item = self.queue[max]
        del self.queue[max]
        return item
        