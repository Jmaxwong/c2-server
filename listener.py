import base64, os
import flask
import os
import sys


class Listener:
    def __init__(self, name, port, ip):
        self.name = name
        self.port = port
        self.ip = ip
        self.pathname = "data/listeners/{}/".format(self.name)#listener 
        #self.keyPath = "{}key".format(self.Path)
        #self.filePath = "{}files".format(self.Path)
        #self.agentsPath = "{}agents/".format(self.Path)

        if os.path.exists("data/listeners/{}/".format(self.name)) == False:
            os.mkdir("data/listeners/{}/".format(self.name))
        
        if os.path.exists("{}key".format(self.pathname)) == False:
            key = 0 #create function for key
            self.key = key

            file = open("{}key".format(self.pathname),'wt')
            try:
                file.write(key)
            except:
                print("Error: Unable to write file")
            file.close()

        else:
            file = open("{}key".format(self.pathname), 'rt')
            try:
                self.key = file.read()
            except:
                print("Error: Unable to read file")

        if os.path.exists("{}agents/".format(self.pathname)) == False:
            os.mkdir("{}agents/".format(self.pathname))

        if os.path.exists("{}files".format(self.pathname)) == False:
            os.mkdir("{}files".format(self.pathname))

        @self.app.route("/reg", methods=['POST'])
        def registerAgent():
            name = flask.request.form.get("name")
            remoteip = flask.request.remote_addr
            hostname = flask.request.form.get("name")
            Type = flask.request.form.get("type")
            print("Agent {} has checked in".format(name))
            #add all agent data into a database
            return(name, 200)#????

