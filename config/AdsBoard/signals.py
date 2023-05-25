from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from .models import Reply
from .tasks import new_reply_notify, reply_status_notify


@receiver(post_save, sender=Reply)
def new_reply_notification(instance, created, **kwargs):
    if created:
        reply_id = Reply.objects.get(id=instance.id).id
        new_reply_notify.delay(reply_id=reply_id)


@receiver(pre_save, sender=Reply)
def reply_status_notification(instance, **kwargs):
    if not Reply.objects.filter(id=instance.id):
        return

    old_repl = Reply.objects.get(id=instance.id)

    if not old_repl.is_approved and instance.is_approved:
        status = 'approved!'
        reply_status_notify.delay(old_repl.id, status)

    elif not old_repl.is_rejected and instance.is_rejected:
        status = 'rejected.'
        reply_status_notify.delay(old_repl.id, status)
