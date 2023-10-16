from flask import Blueprint, abort, redirect, render_template,request, session, url_for,current_app
from jinja2 import TemplateNotFound
from pyrebase import pyrebase
from google.cloud import firestore
from werkzeug.utils import secure_filename
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from flask_mail import Message


# Configuration and Initialize firebase
config = {
  "apiKey": "AIzaSyAPy27QXRyF66zTNI8_7YL6VPy6_fV1YN0",
  "authDomain": "kingsbiz.firebaseapp.com",
  "projectId": "kingsbiz",
  "storageBucket": "kingsbiz.appspot.com",
  "messagingSenderId": "759077597041",
  "appId": "1:759077597041:web:0c7aab9c764499cacf50d0",
  'databaseURL':''
    
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

cred = credentials.Certificate('./key/credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()



# Registering our urls
views = Blueprint(__name__,"views")

# home page route
@views.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)
        
# Login page route
@views.route('/auth-view')
def auth_view():
    try:
        return render_template('login.html')
    except TemplateNotFound:
        abort(404)
# Dashboard Page Route
@views.route('/dashboard', methods=['GET'])
def dash_view():
    if auth.current_user != None:

        return render_template('dashboard-user.html', profile_data=profile_data)

    return render_template('login.html', user_not_authenticated=True)
   

# Employment page route
@views.route('/employ-form')
def employee_form():
    try:
        return render_template('employment.html')
    except TemplateNotFound:
        abort(404)   

@views.route('/authenticate', methods=['GET','POST'])
def authenticate():
    if request.method == 'POST' or request.method == 'GET':
        email = request.form['email']
        password = request.form['password']
        
        if email == 'admin@angels4kings.com':
            # Authenticate as admin
            try:
                # Login the user
                user = auth.sign_in_with_email_and_password(email, password)
                
                # Set the session
                user_id = user['idToken']
                user_email = email
                session['usr'] = user_id
                session['email'] = email
                
                # Redirect admin to admin dashboard
                return render_template("dashboard-admin.html", success_message='You have successfully logged in')
                
            except:
                return render_template('login.html', error_message="Bad credentials. Contact the administrator")
        else:
            # Authenticate as user
            try:
                # Login the user
                user = auth.sign_in_with_email_and_password(email, password)
                
                # Set the session
                user_id = user['idToken']
                user_email = email
                session['usr'] = user_id
                session['email'] = email
                
                # Fetch all profile data from the 'profiles' collection
                profiles_ref = db.collection('profiles')
                profiles = profiles_ref.get()

                # Create an empty list to store the profile data
                profile_data = []

                # Iterate over the profiles and extract the necessary data
                for profile in profiles:
                    data = profile.to_dict()
                    profile_data.append(data)
                            
                
                
                # Redirect regular user to user dashboard
                return render_template("dashboard-user.html", success_message='You are logged in successfully to angels paradise',profile_data=profile_data)
                
            except:
                return render_template('login.html', error_message="Bad credentials. Contact the administrator")
    
    return render_template('login.html')
   
# Logout page route  
@views.route('/logout')
def logout():
    # remove the token setting the user to None
    auth.current_user = None
    # Clear session
    session.clear()
    
    # Redirect the user to the login page with a success message
    return render_template('index.html', success_message='You have successfully logged out from Angels Paradise')

@views.route('/create', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form['title']
        description = request.form['description']
        per_two_hour = request.form['per_two_hour']
        per_four_hour = request.form['per_four_hour']
        overnight = request.form['overnight']
        per_day = request.form['per_day']
        weekend = request.form['weekend']
        weekly = request.form['weekly']
        profile_picture = request.files['profile_picture']
        filename = secure_filename(profile_picture.filename)
        profile_picture.save(os.path.join('./static/uploads', filename))

        # Create a dictionary with the data
        profile_data = {
            'title': title,
            'description': description,
            'charges': {
                'per_two_hour': per_two_hour,
                'per_four_hour': per_four_hour,
                'overnight': overnight,
                'per_day': per_day,
                'weekend': weekend,
                'weekly': weekly
            },
            'profile_picture': filename
        }

        # Store the data in Firebase
        db.collection('profiles').add(profile_data)

        # Return a success message or redirect to another page
        return render_template("dashboard-admin.html", success_message='Created successfully')

    return render_template('create-profile.html')
