import os
from email import encoders
from email.mime.base import MIMEBase

from dotenv import load_dotenv
import tkinter as tk
from tkinter import LEFT
import tkinter.messagebox

class EmailHelper:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.smtp_server = "smtp.yandex.ru"
        self.smtp_port = 587

    def send_email(self, to, subject, filename):
        import smtplib
        from email.mime.multipart import MIMEMultipart

        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to
            msg['Subject'] = subject

            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(filename, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="WorkBook3.xlsx"')
            msg.attach(part)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, to, text)
            server.quit()
            return True
        except Exception as e:
            tk.messagebox.showerror("Ошибка", e)
            return False

    @staticmethod
    def validate_email(email):
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
