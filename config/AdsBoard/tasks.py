from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import Reply


@shared_task
def new_reply_notify(reply_id):
    repl = Reply.objects.get(id=reply_id)
    ad = repl.adv
    ad_author = ad.author.username
    ad_title = ad.title
    repl_text = repl.text
    repl_author = repl.author.username
    ad_author_email = ad.author.email

    mail_subj = 'New reply to your ad!'
    message = render_to_string(
        template_name='AdsBoard/new_reply_email.html',
        context={
            'ad_author': ad_author,
            'ad_title': ad_title[:25] + '...',
            'reply_text': repl_text[:50] + '...',
            'reply_author': repl_author,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[ad_author_email],
    )
    email.send()


@shared_task
def reply_status_notify(reply_id, status):
    repl = Reply.objects.get(id=reply_id)
    repl_author_name = repl.author.username
    repl_text = repl.text
    ad = repl.adv
    ad_title = ad.title
    ad_author = ad.author.username
    repl_author_email = repl.author.email

    mail_subj = 'Your reply status changed'
    message = render_to_string(
        template_name='AdsBoard/reply_status_changed_email.html',
        context={
            'ad_author': ad_author,
            'ad_title': ad_title[:25] + '...',
            'reply_text': repl_text[:50] + '...',
            'reply_author': repl_author_name,
            'status': status,
        },
    )
    email = EmailMessage(
        subject=mail_subj,
        body=message,
        to=[repl_author_email],
    )
    email.send()
