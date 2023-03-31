from flask import Flask, request
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

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