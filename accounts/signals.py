from .models import CustomUser, OTPToken, Profile, Opportunity, Status
from django.core.mail import send_mail
from django.utils import timezone
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
import random
import mailtrap as mt
from decouple import config
from django.contrib.auth import get_user_model
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.html import strip_tags


User = get_user_model()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_token(sender, instance, created, **kwargs):
#     print(instance.is_superuser)
#     if created:
#         if instance.is_superuser == True:
#             pass
#         else:
#             OTPToken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
#             instance.is_active = False
#             instance.save()

#         otp = OTPToken.objects.filter(user=instance).last()
#         subject = "Email Verification"
#         message = f""" 
#                                 Hi {instance.username}, here is your OTP {otp.otp_code}
#             It expires in 5 minutes, use the url below to redirect back to the website
#             http://127.0.0.1:8000/verify-email/{instance.username}"""
#         sender = settings.DEFAULT_FROM_EMAIL
#         recipient = [instance.email]

#         send_mail(subject, message, sender, recipient, fail_silently=False)



# @receiver(user_logged_in)
# def send_otp_on_login(sender, user, request, **kwargs):
#     # Generate OTP
#     # otp = ''.join(random.choices('0123456789', k=6))  # Generate a 6-digit OTP
#     # print("userrrr", user)

#     otp = OTPToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
#     message = f""" 
#                     Hi {user}, here is your OTP {otp.otp_code}
#             It expires in 5 minutes, use the url below to redirect back to the website
#             http://127.0.0.1:8000/accounts/verify/otp/"""

#     # Send OTP to user's email
#     # subject = 'Login OTP'
#     # message = f'Your OTP for login is: {otp}'
#     # from_email = settings.EMAIL_HOST_USER
#     # to_email = user.email
#     # send_mail(subject, message, from_email, [to_email])

#     mail = mt.Mail(
#             sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
#             to=[mt.Address(email=user.email)],
#             subject="Login OTP",
#             text=message,
#             category="Integration Test",
#         )

#     client = mt.MailtrapClient(token=config("MAILTRAP_TOKEN"))
#     client.send(mail)


# message = render_to_string('accounts/email_confirmation.html', {
# #             'user': instance,
# #             'domain': 'localhost:8000',
# #             'uid' : uid,
# #             'token': token
# #         }) 
           
# #             plain_message = strip_tags(message)


# @receiver(user_logged_in)
# def send_otp_on_login(sender, user, request, **kwargs):
#     otp = OTPToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
#     email_message = f""" 
#                     Hi {user}, here is your OTP {otp.otp_code}
#             It expires in 5 minutes, use the url below to redirect back to the website
#             http://127.0.0.1:8000/accounts/verify/otp/"""
#     message = Mail(
#     from_email=config('FROM_EMAIL'),
#     to_emails=[user.email],
#     subject='Login OTP',
#     html_content = f"""
#     <strong>Hi {user.username},</strong><br><br>
#     Here is your OTP: <strong>{otp.otp_code}</strong><br>
#     It expires in 5 minutes.<br><br>
#     Use the URL below to redirect back to the website:<br>
#     <a href="http://127.0.0.1:8000/accounts/verify/otp/">http://127.0.0.1:8000/accounts/verify/otp/</a>
#     """)

#     try:
#         sg = SendGridAPIClient(config('ZEEMY_SENDGRID_API_KEY'))
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e.message)


@receiver(user_logged_in)
def send_otp_on_login(sender, user, request, **kwargs):
    otp = OTPToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
    

    try:
        email = user.email
        subject = "Login OTP"
        message = render_to_string("accounts/otp_login.html", {"username": user.username, "otp_code": otp.otp_code})
        plain_message = strip_tags(message)
        from_email = config('FROM_EMAIL') 
        to = email
        send_mail(subject, plain_message, from_email, [to], html_message=message)
    except Exception as e:
        raise e
         

     


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    # Perform actions you want when a user logs in
    print(f"User {user.username} logged in.")




@receiver(post_save, sender=Opportunity)
def create_opprtunity_status(sender, instance, created, **kwargs):
    if created:
        Status.objects.create(opportunity=instance)


@receiver(post_save, sender=Opportunity)
def save_opprtunity_status(sender, instance, created, **kwargs):
        instance.status.save()





    