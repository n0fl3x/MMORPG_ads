from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import Reply
from .tasks import new_reply_notify, reply_status_notify


@receiver(post_save, sender=Reply)
def new_reply_notification(instance, created, **kwargs):
    if created:
        repl = Reply.objects.get(id=instance.id)
        ad = repl.adv
        ad_author = ad.author.username
        ad_title = ad.title
        repl_text = repl.text
        repl_author = instance.author.username
        ad_author_email = ad.author.email

        new_reply_notify.delay(
            ad_author=ad_author,
            ad_title=ad_title,
            reply_text=repl_text,
            reply_author=repl_author,
            email=ad_author_email
        )


@receiver(pre_save, sender=Reply)
def reply_status_notification(instance, **kwargs):
    if not Reply.objects.filter(id=instance.id):
        return

    old_repl = Reply.objects.get(id=instance.id)
    repl_author = old_repl.author.username
    repl_text = old_repl.text
    ad = old_repl.adv
    ad_title = ad.title
    ad_author = ad.author.username
    email = old_repl.author.email

    if not old_repl.is_approved and instance.is_approved:
        status = 'approved!'

        reply_status_notify.delay(
            reply_author=repl_author,
            reply_text=repl_text,
            ad_title=ad_title,
            ad_author=ad_author,
            status=status,
            email=email,
        )

    elif not old_repl.is_rejected and instance.is_rejected:
        status = 'rejected.'

        reply_status_notify.delay(
            reply_author=repl_author,
            reply_text=repl_text,
            ad_title=ad_title,
            ad_author=ad_author,
            status=status,
            email=email,
        )
