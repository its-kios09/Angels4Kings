from flask import Blueprint, render_template,request
from pyrebase import pyrebase

# Initializing pyrebase
# Initialize firebase
config = {
    'apiKey': "AIzaSyBPnqa2PdpSnipXI1S407rfIHFYEY4aWp8",
    'authDomain': "kingsauth-67a90.firebaseapp.com",
    'projectId': "kingsauth-67a90",
    'storageBucket': "kingsauth-67a90.appspot.com",
    'messagingSenderId': "698579119515",
    'appId': "1:698579119515:web:81f6f24d1225745278053e",
    'measurementId': "G-XHE0YBHKDH",
     'databaseURL':''
    
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


views = Blueprint(__name__,"views")
# Defining our routes
# home page route
@views.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)

@views.route('/auth-view')
def auth_view():
    try:
        return render_template('login.html')
    except TemplateNotFound:
        abort(404)
        
@views.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = firebase.auth().sign_in_with_email_and_password(email, password)
        # If the login is successful, render the dashboard-user.html template
        return render_template('dashboard-user.html')
    except pyrebase.AuthError as e:
        error_message = e.args[1]
        # Handle the authentication error, such as displaying an error message to the user
        return render_template('login.html', error=error_message)