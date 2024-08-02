from flask_mail import Message
from flask import current_app, render_template, url_for
from app import mail

def send_reset_email(user_email, token):
    msg = Message('Password Reset Request',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user_email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('api.auth_reset_password', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)