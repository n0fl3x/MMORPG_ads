from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .passwords import one_time_password
from .models import UsersCode, User


@shared_task
def new_user_conf_code_mail(user_id):
    conf_code = one_time_password()
    new_user = User.objects.get(id=user_id)
    new_user_code = UsersCode.objects.create(user=new_user, code=conf_code)
    new_user_name = new_user_code.user.username
    new_user_email = new_user_code.user.email

    mail_subj = 'Acccount confirmation'
    message = render_to_string(
        template_name='accounts/account_activate_email.html',
        context={
            'username': new_user_name,
            'conf_code': conf_code,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[new_user_email],
    )
    email.send()


@shared_task
def non_activated_user_conf_code_mail(user_id):
    new_conf_code = one_time_password()
    non_activated_user = User.objects.get(id=user_id)
    old_conf_code = UsersCode.objects.get(user=non_activated_user)
    old_conf_code.code = new_conf_code
    old_conf_code.save()
    non_activated_username = non_activated_user.username
    non_activated_email = non_activated_user.email

    mail_subj = 'New confirmation code'
    message = render_to_string(
        template_name='accounts/account_activate_email.html',
        context={
            'username': non_activated_username,
            'conf_code': new_conf_code,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[non_activated_email],
    )
    email.send()


@shared_task
def weekly_non_active_users_and_codes_clear():
    non_active_users = User.objects.filter(is_active=False)
    for user in non_active_users:
        user.delete()

    unused_codes = UsersCode.objects.all()
    for code in unused_codes:
        code.delete()
