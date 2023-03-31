from flask import Flask, request, send_from_directory
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET', 'POST'])
def index():
    return send_from_directory('static', 'index.html')


@app.route('/submit', methods=['POST'])
def handle_form_submission():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    from_email = os.environ.get('FROM_EMAIL')
    to_email = os.environ.get('TO_EMAIL')
    subject = 'New message from your website!'
    body = f'Name: {name}\nEmail: {email}\n\n{message}'

    headers = {
        'Authorization': f'Bearer {sendgrid_api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": to_email
                    }
                ],
                "subject": subject
            }
        ],
        "from": {
            "email": from_email
        },
        "content": [
            {
                "type": "text/plain",
                "value": body
            }
        ]
    }

    response = requests.post('https://api.sendgrid.com/v3/mail/send', json=data, headers=headers)

    if response.status_code == 202:
        return "Message sent successfully!"
    else:
        return f"Error sending message: {response.text}"


if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 8000)))
