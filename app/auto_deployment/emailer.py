import ssl
import smtplib
from email.message import EmailMessage

# Used for reference: https://youtu.be/g_j6ILT-X0k?si=r_8WgLATGqvO39AF
def send_email(subject, body):
    email_sender = 'ci.cd.team4@gmail.com'
    email_password = 'nxhrtwymbywcdhzv'
    email_receivers = ['rishabh.thaney@mail.mcgill.ca', 'aayush.kapur@mail.mcgill.ca', 'varun.shiri@mail.mcgill.ca']

    subject = subject
    body = body

    for email_receiver in email_receivers:
        mail_param = EmailMessage()
        mail_param['From'] = email_sender
        mail_param['To'] = email_receiver
        mail_param['Subject'] = subject
        mail_param.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, mail_param.as_string())