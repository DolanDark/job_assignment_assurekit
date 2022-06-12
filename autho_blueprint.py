import pyrebase
from flask import Blueprint, render_template, request, flash, session, redirect, url_for

autho = Blueprint("autho", __name__)
print("autho_blueprint executed")

firebase_config = {
  "apiKey": "AIzaSyC6izH7bqmq-EQY6JbhFPRxFIGzMZWrLK8",
  "authDomain": "akash-test-338618.firebaseapp.com",
  "projectId": "akash-test-338618",
  "storageBucket": "akash-test-338618.appspot.com",
  "messagingSenderId": "217507775389",
  "appId": "1:217507775389:web:75533c3b53d8fa81f4e574",
  "databaseURL": ""
  }

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

from app import cross_origin, db

autho.secret_key = 'secretval'


@autho.route("/", methods=["GET","POST"])
@autho.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            check_auth = auth.sign_in_with_email_and_password(email, password)

            if check_auth['registered']:
                session['user'] = email
                flash('Logged in successfully!', category='success')
                return redirect(url_for('data_blueprint.user_page'))
            else:
                flash('Incorrect password, try again.', category='error')
        except:
            flash('Incorrect password, try again.', category='error')
    return render_template("login.html", user = "logging_in")


@autho.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':

        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        get_user = db.execute("SELECT 1 FROM assurekit_users WHERE email=%s", (email,))

        if get_user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = auth.create_user_with_email_and_password(email, password1)
            uid = new_user['localId']
            new_user_query = db.run("INSERT INTO assurekit_users (userid, username, email, isadmin) VALUES (%s,%s,%s,%s)", (uid, first_name, email, False))
            logging_in = auth.sign_in_with_email_and_password(email, password1)
            session['user'] = email
            flash('Account created!', category='success')
            return redirect(url_for('data_blueprint.user_page'))
    
    return render_template("signup.html", user="signed_up")


@autho.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('autho.login'))

@autho.route("/info")
def info():
    return render_template("info.html", user="temp")

