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
    personality_info = db.relationship("Personality", backref="personality", uselist=False, single_parent=True)

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
    id = db.Column(db.INTEGER, db.ForeignKey(User.id), primary_key=True)
    # username = db.Column(db.String(64), db.ForeignKey(User.username), unique=True,nullable=False)
    personality_type = db.Column(db.String(5))
    personality_preference = db.Column(db.String(40))

    introvert = db.Column(db.String(50), unique=False)
    extrovert = db.Column(db.String(50), unique=False)
    sensing = db.Column(db.String(50), unique=False)
    intuition = db.Column(db.String(50), unique=False)

    thinking = db.Column(db.String(50), unique=False)
    feeling = db.Column(db.String(50), unique=False)
    judging = db.Column(db.String(50), unique=False)
    perceiving = db.Column(db.String(50), unique=False)


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
'''
prof = Professor(username='admin',password='admin')
db.session.add(prof)
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
api_manager.create_api(User, methods=['GET', 'POST'],exclude_columns = ["password"])


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect('/login')

    elif session['user']:
        prof = Professor.query.filter_by(username=session['user']).first()
        print "-----------0000---------------"
        if prof is None:
            print 'going back!'
            return login()
        else:
            print prof.username
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
        print session['user']
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
            flash('Login Successful for user "%s"' % (form.username.data))
            # flash('Login Successful for user "%s" with password "%s"' % (form.username.data, str(form.password.data)))
            return redirect('/index')

        else:
            print type(form.password.errors)
            print form.password.errors.append("Please enter valid credentials")

    return render_template('login.html', title='Sign In', form=form)


# Empty for now
@app.route('/analyze', methods=['GET'])
def analyze():
    if 'user' not in session:
        return redirect('/')
    elif 'user' in session:
        all_users = User.query.all()
        all_personality = Personality.query.all()
        '''
        for user in all_users:
            if user.basic_info is None:
                user.basic_info = 'N/A'
        '''

        return render_template('analyze.html', all_users=all_users, all_personality=all_personality)
    return redirect('/')


'''
@app.route('/analysis/<analyze_user>')
'''


@app.route('/analysis/<user_name>')
def analysis(user_name):
    if 'user' not in session:
        return redirect('/')
    elif 'user' in session:
        print 'hello to analysis'
        return render_template('analysis.html', analysis_name=user_name)
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
        # print request.headers.get()
        json = request.json
        print(json)
        # Render template
        post_username = json.get("username")
        print post_username
        post_email = json.get("email")
        print post_email
        post_password = json.get("password")
        print post_password
        purpose = json.get("purpose")

        my_message = "default"
        allow = False

        post_users = User.query.all()
        print post_users
        print purpose

        if purpose == 'signup':
            post_fname = json.get("basic_info").get("fname")
            post_lname = json.get("basic_info").get("lname")
            post_enrollment = json.get("basic_info").get("enrollment")
            post_dept = json.get("basic_info").get("dept")
            post_age = json.get("basic_info").get("age")
            post_cpi = json.get("basic_info").get("cpi")
            post_backlogs = json.get("basic_info").get("backlogs")
            post_transport = json.get("basic_info").get("transport")
            post_fav_subjects = json.get("basic_info").get("fav_subjects")
            post_gender = json.get("basic_info").get("gender")

            print 'inside signup'
            if post_users:
                for one_user in post_users:
                    print one_user
                    if (post_username == one_user.username) or (post_email == one_user.email):
                        allow = False
                        my_message = "Account already exists!"
                        print my_message
                        break
                    else:
                        allow = True
                        print "so good"

            if allow or not post_users:
                b1 = BasicInfo(first_name=post_fname, last_name=post_lname, enrollment=post_enrollment,
                               department=post_dept, age=post_age, CPI=post_cpi, backlogs=post_backlogs,
                               transport=post_transport, fav_subjects=post_fav_subjects, gender=post_gender)
                u1 = User(username=post_username, email=post_email, password=post_password, basic_info=b1)
                db.session.add(u1)

                try:
                    db.session.commit()
                    my_message = "Account successfully created"
                except Exception, err:
                    print Exception, err
                    my_message = "There was a problem"

        if purpose == 'signin':
            for one_user in post_users:
                print one_user
                if (one_user.username == post_username):
                    correctUser = True
                    if (one_user.password == post_password):
                        correctPassword = True
                        my_message = "Login successful"
                        print my_message
                        break
                    elif(one_user.password != post_password):
                        correctPassword = False
                        my_message = "Please check your password"
                        break
                else:
                    allow = False
                    my_message = "User does not exist!"
                    print "not so good while singing in"


                # correct this------------------------------------------
        if purpose == 'personality':

            #Not going to nest here

            post_personality_type = json.get("personality_type")
            post_personality_preference = json.get("personality_preference")
            post_introvert = json.get("introvert")
            post_extrovert = json.get("extrovert")
            post_sensing = json.get("sensing")
            post_intuition = json.get("intuition")
            post_thinking = json.get("thinking")
            post_feeling = json.get("feeling")
            post_judging = json.get("judging")
            post_perceiving = json.get("perceiving")

            my_user = User.query.filter_by(username = post_username).first()
            print "MyUserIsHere"
            print post_introvert
            if my_user.personality_info is None:
                b = Personality(id = my_user.id,personality_type = post_personality_type,
                                personality_preference=post_personality_preference,
                                introvert = post_introvert,extrovert = post_extrovert,
                                sensing = post_sensing, intuition = post_intuition,
                                thinking = post_thinking, feeling = post_feeling,
                                judging = post_judging, perceiving = post_perceiving)
                db.session.add(b)
                db.session.commit()
                my_message = "inserted"
            else:
                my_user.personality_info.personality_type = post_personality_type
                my_user.personality_info.personality_preference = post_personality_preference

                my_user.personality_info.introvert = post_introvert
                my_user.personality_info.extrovert = post_extrovert

                my_user.personality_info.sensing = post_sensing
                my_user.personality_info.intuition = post_intuition

                my_user.personality_info.thinking= post_thinking
                my_user.personality_info.feeling = post_feeling

                my_user.personality_info.judging = post_judging
                my_user.personality_info.perceiving= post_perceiving

                db.session.commit()
                my_message = "inserted"
            #db.session.add(my_user.personality_info.personality_type)

        if purpose == 'welcome':
            for one_user in post_users:

                if (post_username == one_user.username) or (post_email == one_user.email):
                    allow = False
                    my_message = "Account already exists"
                    print my_message
                    break
                else:
                    allow = True
                    print "so good"
            if allow:
                my_message = "You may proceed"
        print my_message
        return my_message

    # return jsonify(json)
    elif request.method == 'GET':
        return redirect('/404')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0")
    # app.run(host="0.0.0.0")
