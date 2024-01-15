import numpy as np
from message import Message

class Swp:
    def __init__(self, path, width, length):
        self.path = path
        self.width = width
        self.length = length

class Node:

    def __init__(self, id):
        self.id = id
        self.ins = {}
        self.stab_time = 0
        self.updated = False
        self.wsp = {
            'path': '',
            'width': 0,
            'length': np.inf
        }
        self.naive_swp = {
            'path': '',
            'width': 0,
            'length': np.inf
        }
        self.swp = Swp('', 0, np.inf)
        self.swps = [self.swp]

    
    def nullify(self):
        self.wsp = {
            'path': '',
            'width': 0,
            'length': np.inf
        }
        self.naive_swp =  {
            'path': '',
            'width': 0,
            'length': np.inf
        }
        self.updated = False
        self.stab_time = 0
        self.swp = Swp('', 0, np.inf)
        self.swps = [self.swp]
        

    def add_ins(self, in_id, in_width, in_len):
        self.ins[in_id] = (in_width, in_len)
    

    def compare_wsp(self, v, w, l):
        if self.wsp['length'] > v.wsp['length'] + l:
            self.wsp['length'] = v.wsp['length'] + l
            self.wsp['width'] = min(v.wsp['width'], w)
            self.wsp['path'] = v.wsp['path'] + ',' + self.id

            self.updated = True

        elif self.wsp['length'] == v.wsp['length'] + l and self.wsp['width'] < min(v.wsp['width'], w):
            self.wsp['length'] = v.wsp['length'] + l
            self.wsp['width'] = min(v.wsp['width'], w)
            self.wsp['path'] = v.wsp['path'] + ',' + self.id

            self.updated = True
        
        else: self.updated = False


    def compare_naive_swp(self, v, w, l):
        if self.naive_swp['width'] < min(v.naive_swp['width'], w):
            self.naive_swp['length'] = v.naive_swp['length'] + l
            self.naive_swp['width'] = min(v.naive_swp['width'], w)
            self.naive_swp['path'] = v.naive_swp['path'] + ',' + self.id

            self.updated = True

        elif self.naive_swp['width'] == min(v.naive_swp['width'], w) and self.naive_swp['length'] > v.naive_swp['length'] + l:
            self.naive_swp['length'] = v.naive_swp['length'] + l
            self.naive_swp['width'] = min(v.naive_swp['width'], w)
            self.naive_swp['path'] = v.naive_swp['path'] + ',' + self.id

            self.updated = True
        
        else: self.updated = False

    
    def compare_swp(self, v, w, l):
        for p in v.swps:
            if self.id not in p.path:
                temp_path = p.path + ',' + self.id
                temp_width = min(p.width, w)
                temp_length = p.length + l

                #if len([n for n in self.swps if n.path == p.path and n.width == p.width and n.length == p.length]) == 0:
                self.swps.append(Swp(temp_path, temp_width, temp_length))
                self.updated = True
            
            else: self.updated = False
        
        widest = self.swp.width
        shortest = self.swp.length
        path = self.swp.path

        for p in self.swps:
            if p.width > widest:
                widest = p.width
                shortest = p.length
                path = p.path

            elif p.width == widest and p.length < shortest:
                shortest = p.length
                path = p.path
               
        self.swp = Swp(path, widest, shortest)


        