from flask_mail import Message
from application import mail
from flask import current_app

def send_email(to, subject, html_body, attachments=None):
    msg = Message(
        subject=subject,
        recipients=to,
        sender=current_app.config["MAIL_DEFAULT_SENDER"]
    )
    if attachments:
        for filename, file_bytes, mimetype in attachments:
            msg.attach(filename, mimetype, file_bytes)

    msg.html = html_body
    mail.send(msg)
