import smtplib
from api_keys import api_keys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class MailEngine:
    def __init__(self):
        self.email = api_keys["gmail"]
        self.pwd = api_keys["gpwd"]
        self.smtp = "smtp.gmail.com"

    def send_email(self, to, subject, body):
        with smtplib.SMTP(self.smtp) as conn_mail:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.email
            msg["To"] = to
            msg_text = MIMEText(body, 'plain')
            msg.attach(msg_text)
            conn_mail.starttls()
            conn_mail.login(user=self.email, password=self.pwd)
            conn_mail.sendmail(from_addr=self.email,
                               to_addrs=to,
                               msg=msg.as_string()
                               )

        print("Mail sent")

