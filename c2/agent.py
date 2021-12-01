import os
import sys


class Agent:
    def __init__(self, name, listener, ip, hostname, key):
        self.name = name
        self.listener = listener
        self.ip = ip
        self.hostname = hostname
        self.key = key
        self.timesleep = 100 #adjustable variable for implant sleep
        self.pathname = "data/listeners/{}/agents/{}/".format(self.listener, self.name)
        self.commands = {} #TODO: change this to array of commands

        if os.path.exists(self.pathname)== False:
            os.mkdir(self.pathname)
        
        

        
