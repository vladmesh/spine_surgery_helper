import os


class EmailHelper:
    def __init__(self):
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.smtp_ssl = os.getenv('SMTP_SSL')

    def send_email(self, to, subject, message):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, to, text)
            server.quit()
            return True
        except:
            return False

    @staticmethod
    def validate_email(email):
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
