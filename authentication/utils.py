from django.core.mail import EmailMessage

#this class will help us send email
class Util:
    @staticmethod #this decorator helps us use this class method send_email without instantiating the class itself
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()
