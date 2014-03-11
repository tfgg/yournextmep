import uuid
import smtplib

from datetime import datetime

from pymongo import MongoClient
from flask import Flask, url_for, render_template, request, abort, jsonify
from flask.ext.mail import Mail, Message

import settings

db_client = MongoClient()
app = Flask(__name__)

app.config.update(
  MAIL_SERVER=settings.MAIL_SERVER,
  MAIL_PORT=settings.MAIL_PORT,
  MAIL_USE_SSL=settings.MAIL_USE_SSL,
  MAIL_USERNAME=settings.MAIL_USERNAME,
  MAIL_PASSWORD=settings.MAIL_PASSWORD
  )

mail = Mail(app)

db_subscriptions = db_client.ochlo.newsletter_subscriptions

def get_context():
  return {'CONTACT_EMAIL': settings.CONTACT_EMAIL,
          'BASE_URL': settings.BASE_URL,
          'REDIRECT_LINK': settings.REDIRECT_LINK,}

@app.route('/subscribe', methods=['POST'])
def subscribe():
  email_address = request.form.get('email', '').strip()

  if "@" not in email_address:
    return jsonify({'error_text': "That doesn't look like an email address."})

  num_found = db_subscriptions.find({'email_address_lower': email_address.lower()}).count()

  if num_found == 0:
    confirmation_token = str(uuid.uuid4())
    unsubscribe_token = str(uuid.uuid4())

    subscribe_doc = {'email_address': email_address,
                     'email_address_lower': email_address.lower(),
                     'time_added': datetime.now(),
                     'confirmed': False,
                     'confirmation_token': confirmation_token,
                     'active': False,
                     'unsubscribe_token': unsubscribe_token,
                     }

    msg = Message('Confirm your subscription',
                  sender='timothy.green@gmail.com',
                  recipients=[email_address])

    msg.body = render_template('subscribe_email.txt',
                               doc=subscribe_doc,
                               **get_context())
    try:
      mail.send(msg)
    except smtplib.SMTPRecipientsRefused:
      return jsonify({'error_text': "There was an error sending to {}.".format(email_address)})
    
    db_subscriptions.insert(subscribe_doc)

    return jsonify({'success_text': 'Successfully subscribed. Thank you!'})
  else:
    return jsonify({'error_text': "The email address {} is already subscribed!".format(email_address)})


@app.route('/confirm/<confirmation_token>')
def confirm(confirmation_token):
  doc = db_subscriptions.find_one({'confirmation_token': confirmation_token})

  if doc is not None:
    doc['confirmed'] = True
    doc['active'] = True
    doc['time_confirmed'] = datetime.now()
    db_subscriptions.save(doc)

    return render_template('confirm_success.html',
                           **get_context())
  else:
    return render_template('confirm_failure.html',
                           **get_context())

@app.route('/unsubscribe/<unsubscribe_token>', methods=['POST','GET'])
def unsubscribe_by_token(unsubscribe_token):
  doc = db_subscriptions.find_one({'unsubscribe_token': unsubscribe_token})

  if doc is not None:
    confirm = (request.form.get('confirm', False) == 'yes')

    print confirm

    if not confirm:
        return render_template('unsubscribe.html',
                               doc=doc)
    else:
        doc['unsubscribe_feedback'] = request.form.get('feedback', None)
        doc['active'] = False
        doc['time_unsubscribed'] = datetime.now()
        db_subscriptions.save(doc)

        return render_template('unsubscribe_success.html',
                               doc=doc,
                               **get_context())
  else:
      return render_template('unsubscribe_failure.html',
                             message='Could not find unsubscribe token. Is the link correct?',
                             **get_context())

if __name__ == "__main__":
  app.run(debug=True)

