import smtplib

MY_EMAIL = "SENDER EMAIL"
MY_SMTP = "smtp.gmail.com"
PASSWORD = "SENDER PASSWORD"


class NotificationManager:
    # sending notifications with the deal flight details.

    def send_email(self, message, email_list):
        for user_email in email_list:
            with smtplib.SMTP(MY_SMTP) as email:
                email.starttls()
                email.login(user=MY_EMAIL, password=PASSWORD)
                email.sendmail(from_addr=MY_EMAIL, to_addrs=user_email,
                               msg=message)