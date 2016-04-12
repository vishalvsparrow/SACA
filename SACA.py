from flask import Flask, jsonify
from flask import flash, redirect, request, session
from forms import LoginForm
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager
from flask import render_template, abort
from jinja2 import TemplateNotFound

# from models import db

'''
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
'''

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'
# db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=False)
    basic_info = db.relationship("BasicInfo", uselist=False, backref="user", single_parent=True)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Professor(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64), index=True, unique=False)


class BasicInfo(db.Model):
    __tablename__ = 'Basic Information'
    id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=False)
    last_name = db.Column(db.String(64), index=True, unique=False)
    gender = db.Column(db.String(8), index=True, unique=False)
    enrollment = db.Column(db.String(16), index=True, unique=True)
    department = db.Column(db.String(40), index=True, unique=False)
    age = db.Column(db.INTEGER, index=True, unique=False)
    CPI = db.Column(db.String(5), index=True, unique=False)
    backlogs = db.Column(db.INTEGER, index=True, unique=False)
    transport = db.Column(db.String(20), index=True, unique=False)
    fav_subjects = db.Column(db.String(128), index=True, unique=False)


class Personality(db.Model):
    __tablename__ = 'Personality Information'
    id = db.Column(db.INTEGER,db.ForeignKey(User.id),primary_key =True)
    username = db.Column(db.String(64),db.ForeignKey(User.username),unique=True)
    personality_type = db.Column(db.String(5))
    personality_preference = db.Column(db.String(40))

    introvert = db.Column(db.String(50),unique=False)
    extrovert = db.Column(db.String(50),unique=False)
    sensing = db.Column(db.String(50),unique=False)
    intuition = db.Column(db.String(50),unique=False)

    thinking = db.Column(db.String(50),unique=False)
    feeling = db.Column(db.String(50),unique=False)
    judging = db.Column(db.String(50),unique=False)
    perceiving = db.Column(db.String(50),unique=False)
    


db.create_all()
'''
u = User(username='test', email='test@test.com',password='testing123')
db.session.add(u)
db.session.commit()
'''
'''
u = User.query.all()
for user in u:
    if user.username == 'test':
        myid = user.id

'''

'''
b = BasicInfo(id = myid, first_name='George',last_name = 'Harrison',gender = 'Male',enrollment='82929109',department = 'IT',age=19,CPI='23',backlogs=0,transport='George\'s bus',
              fav_subjects='Music')
u1 = User(username='bandOnTheRun',email='Wings@wing.com',password='sjoksd')
#db.session.add(u1)
db.session.add(b)
db.session.commit()
'''

users = User.query.all()
basic = BasicInfo
for user in users:
    if user.username == 'vishal':
        print user.username
        print user.id
        print user.email
        print user.password

api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(User, methods=['GET', 'POST'])


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect('/login')

    elif session['user']:
        prof = Professor.query.filter_by(username=session['user']).first()
        print prof.username
        print "-----------0000---------------"
        if prof is None:
            return login()
        message = 'Welcome back Professor ' + session['user'].title() + "!"
        return render_template('index.html', title='Home', users=users, basic=basic, message=message)

    '''
    user = {'nickname': 'Vishal'}
    posts = [
        {
            'author': {'nickname':'Joey'},
            'body': {'post_title':'Beach and more in Campbell'}
        },
        {
            'author': {'nickname':'George'},
            'body': {'post_title':'Cool and calm waters of Tampana Haven'}
        }
    ]
    '''

    '''
    if session['user']:
        return render_template('index.html',users = users,basic=basic)
    else:
        print 'IM HERE'
        login()
    '''

    return render_template('index.html', title='Home', user=user, basic='', message='First time ERROR!')


#    return login()

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if 'user' in session:
        return redirect('/')

    if form.validate_on_submit():
        userExists = Professor.query.filter_by(username=form.username.data).first()
        passwordExists = Professor.query.filter_by(password=form.password.data).first()
        print passwordExists
        print userExists
        if userExists and passwordExists:
            print 'exists! login successful!'
            session['user'] = form.username.data
            print 'THIS IS THE COOKIE-->'
            print session['user']
            flash('Login Successful for user "%s" with password "%s"' % (form.username.data, str(form.password.data)))
            return redirect('/index')

        else:
            print type(form.password.errors)
            print form.password.errors.append("Please enter valid credentials")

    return render_template('login.html', title='Sign In', form=form)


# Empty for now
@app.route('/analyze', methods=['GET'])
@app.route('/analyze/', methods=['GET'])
def analyze_general():
    if 'user' not in session:
        return redirect('/')
    elif 'user' in session:
        return render_template('analyze.html')
    return redirect('/')


@app.route('/analyze/<analyze_user>')
def analyze(analyze_user):
    if 'user' not in session:
        return redirect('/')
    elif 'user' in session:
        return render_template('analyze.html', analyze_user=analyze_user)

    return redirect('/')


@app.route('/logout', methods=['GET'])
def logout():
    if 'user' not in session:
        return redirect('/login')
    elif 'user' in session:
        session.pop('user', None)
        return redirect('/login')
    return redirect('/login')


@app.route('/personality')
@app.route('/personality/')
def personality_general():
    if 'user' not in session:
        return redirect('/')
    elif 'user' in session:
        return render_template('personality_types.html')
    return redirect('/login')


@app.route('/personality/<personality>')
@app.route('/personality/<personality>/')
def personality(personality):
    try:
        if 'user' not in session:
            return redirect('/login')
        elif 'user' in session:

            final = '/personality_pages/'
            personality = personality.upper()
            personality += '.html'
            final += personality
            return render_template('personality.html', personality=final)

    except TemplateNotFound:
        abort(404)

    return redirect('/login')


@app.errorhandler(404)
def page_not_found(e):
    if 'user' not in session:
        return redirect('/login')
    return render_template('404.html')


@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'POST':
        # Get the parsed contents of the form data
        json = request.json
        print(json)
        # Render template
        print json.get("username")
        print json.get("password")
        print json.get("basic_info").get("Backlogs")
        return "positive"
    #      return jsonify(json)
    elif request.method == 'GET':
        return redirect('/404')


if __name__ == "__main__":
    # app.run(debug=True, use_reloader=False)
    app.run(host="0.0.0.0")
