from flask import Flask, request, send_from_directory
import smtplib
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    print(smtp_username, smtp_password)
    return send_from_directory('static', 'index.html')

@app.route('/submit', methods=['POST'])
def handle_form_submission():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    
    from_address = smtp_username
    to_address = 'dmccaffrey01@gmail.com'
    subject = 'New message from your website!'
    body = f'Name: {name}\nEmail: {email}\n\n{message}'

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    message = f'Subject: {subject}\n\n{body}'
    server.sendmail(from_address, to_address, message)
    
    server.quit()

    return "Message sent sucessfully!"

if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8000)))