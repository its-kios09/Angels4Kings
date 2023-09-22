from flask import Flask
from views import views
from flask_mail import Mail, Message
from flask import Blueprint, abort, redirect, render_template,request, session, url_for,current_app
from flask import Flask, flash, redirect, render_template, request, url_for



# Initializing flask app

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'mail.angels4kings.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'info@angels4kings.com'
app.config['MAIL_PASSWORD'] = 'Kilonzo.2@'
app.config['MAIL_DEFAULT_SENDER'] = 'info@angels4kings.com'

mail = Mail(app)

# Registering blueprint views
app.register_blueprint(views,url_prefix='/')
# Secret Key
app.secret_key = 'qwertyuiopasdfghjklzxcvbnm'

@app.route('/send_mail', methods=['POST'])
def send_mail():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    msg = Message(subject, recipients=['info@angels4kings.com'])
    msg.body = f"You have received a new message from {email}.\n\nHello Admin,\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}\n\n\n\nBest regards,\nwww.angels4kings.com"

    mail.send(msg)
    return render_template('index.html', success_message='Mail sent successfully')

@app.route('/send_employee', methods=['POST'])
def send_employee():
    # Form data
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    phone = request.form['Phone']

    # Create the email message
    msg = Message(subject, recipients=['info@angels4kings.com'])
    msg.body = f"You have received a new message from {email}.\n\nHello Admin,\n\nName: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}\n\n\n\nBest regards,\nwww.angels4kings.com"

    # Attach files if provided
    for i in range(1, 4):
        file = request.files.get(f'file{i}')
        if file:
            file_data = file.read()
            file_content_type = file.content_type
            file_name = file.filename

            msg.attach(file_name, data=file_data, content_type=file_content_type)

    try:
        mail.send(msg)
        return render_template('index.html', success_message='Mail sent successfully')
    except Exception as e:
        return str(e)



if __name__ == '__main__':
    app.run(debug=True)