from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
import threading

from django.core.mail import EmailMessage, send_mail
# from twilio.rest import Client
from decouple import config



def send_code_to_email(email, code, name="Dude"):
    def send_in_thread():
        subject = "Activation Code"
        from_email = settings.EMAIL_HOST_USER
        to = email
        html_content = render_to_string('activation.html', {"code":code, "name":name})
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    thread = threading.Thread(target=send_in_thread)
    thread.start()

    return True


def send_code_to_phone(phone_number, code):
    # def send_in_thread():
    #     account_sid = config('TWILIO_ID')
    #     auth_token = config('TWILIO_KEY')
    #     client = Client(account_sid, auth_token)

    #     client.messages.create(
    #         from_='+12073877090',
    #         to=phone_number,
    #         body=f"Your activation code is {code}"
    #     )

    # thread = threading.Thread(target=send_in_thread)
    # thread.start()

    # return True
    print("Coming soon!.. (shared/utils.py/send_code...)")
