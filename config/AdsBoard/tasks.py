from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task
def new_reply_notify(ad_author, ad_title, reply_text, reply_author, email):
    mail_subj = 'New reply to your ad!'
    message = render_to_string(
        template_name='AdsBoard/new_reply_email.html',
        context={
            'ad_author': ad_author,
            'ad_title': ad_title[:25] + '...',
            'reply_text': reply_text[:50] + '...',
            'reply_author': reply_author,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[email],
    )
    email.send()


@shared_task
def reply_status_notify(ad_author, ad_title, reply_text, reply_author, status, email):
    mail_subj = 'Your reply status changed'
    message = render_to_string(
        template_name='AdsBoard/reply_status_changed_email.html',
        context={
            'ad_author': ad_author,
            'ad_title': ad_title[:25] + '...',
            'reply_text': reply_text[:50] + '...',
            'reply_author': reply_author,
            'status': status,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[email],
    )
    email.send()
