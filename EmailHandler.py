import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import ssl


class EmailHandler:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password, from_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.from_email = from_email

    @staticmethod
    def has_contact_info(text):

        phone_pattern = r'(?:\+7|8|9)\d{8,}'

        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,10}\b'

        phone_match = re.search(phone_pattern, text)
        email_match = re.search(email_pattern, text)

        result = email_match is not None
        return result

    def send_email(self, to_email, subject, message, user_metadata):
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        message += f"\n\nUser Metadata:\n{user_metadata}"

        msg.attach(MIMEText(message, 'plain'))

        try:
            context = ssl.create_default_context()  # Создайте контекст SSL
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context)  # Используйте SMTP_SSL
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.from_email, to_email, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print("Ошибка при отправке письма:", str(e))
            return False
