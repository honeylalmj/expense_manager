import smtplib
from email.mime.text import MIMEText

def send_email(name,code,patient_id,email):
    
    subject = "Verification code for {}".format(name)
    body = "Your verification code is {} and your patient id is : {}".format(code,patient_id)
    sender = "trackerrehab@gmail.com"
    password = "cpkz tjog coaq uibv"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender,email, msg.as_string())
    print("Message sent!")
