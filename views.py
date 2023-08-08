from flask import Blueprint, render_template

# Initializing pyrebase

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