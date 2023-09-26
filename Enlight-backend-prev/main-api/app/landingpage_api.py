from app import app
from flask import request
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from app.mongo_client import MongoClient, parameters

client = MongoClient().client
db = client[parameters['MONGO_PAGE_DB']]

ses_host = parameters['SES_HOST']
ses_port = parameters['SES_PORT']
ses_username = parameters['SES_USERNAME']
ses_password = parameters['SES_PASSWORD']


def send_email(sender, receiver, subject, content):
    smtphost = ses_host
    port = ses_port
    ese_password = ses_password
    ese_username = ses_username
    message = content
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP(smtphost, 587)
    server.starttls()
    server.login(ese_username, ese_password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    

# This is the landing page API used to track the 
# contact information by the user.
@app.route('/contact-save', methods=['POST'])
def contact_info_process():
    data = request.get_json()
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    message = data['message']
    collection = db['contact_info']
    
    if collection.count_documents({"email": email}) > 100:
        return {"message": "Error! This email has been used more than 100 "+
                "times. Please use another email address."}
    
    collection.insert_one({
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "message": message,
        "datatime": datetime.utcnow()
    })
    
    # Now, let's send an email to the support team.
    sender = "support@enlight-ai.com"
    receiver = "support@enlight-ai.com"
    subject = f"New contact information from {firstname} {lastname}"
    content = f"Name: {firstname} {lastname}"\
              +f"\nEmail: {email}"\
              +f"\nMessage: {message}"
    send_email(sender, receiver, subject, content)
    return {"message": "success"}
    
    
    
    
    


