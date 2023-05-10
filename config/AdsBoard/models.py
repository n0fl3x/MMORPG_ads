from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


CATEGORIES = [
    ('Tank', 'TK'),
    ('Healer', 'HL'),
    ('Damage dealer', 'DD'),
    ('Trader', 'TR'),
    ('Guild master', 'GM'),
    ('Quest giver', 'QG'),
    ('Warsmith', 'WS'),
    ('Tanner', 'TN'),
    ('Potion maker', 'PM'),
    ('Spell master', 'SM'),
]


class Adv(models.Model):
    """Advertising representation class."""

    date_of_creation = models.DateTimeField(
        auto_now_add=True,
    )

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='adv_created_by',
    )

    title = models.CharField(
        max_length=255,
        help_text='Up to 255 symbols',
    )

    category = models.CharField(
        max_length=15,
        choices=CATEGORIES,
        default=None,
    )

    content = RichTextField()

    class Meta:
        verbose_name = 'Advertise'
        verbose_name_plural = 'Advertisements'

    def __str__(self) -> str:
        return f'{self.title}'

    def get_adv_pk(self) -> str:
        return f'{self.id}/'


class Reply(models.Model):
    """Replies class for our advertisements."""

    date_of_creation = models.DateTimeField(
        auto_now_add=True,
    )

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='reply_created_by',
    )

    adv = models.ForeignKey(
        to=Adv,
        on_delete=models.CASCADE,
        related_name='replies_to_adv',
    )

    text = models.TextField()

    approved = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self) -> str:
        return f'Reply #{self.id}'

    def is_approved(self) -> None:
        self.approved = True
        self.save()
