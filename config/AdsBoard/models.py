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

    content = RichTextField(
        blank=True
    )

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

    text = models.TextField(
        blank=True,
    )

    is_approved = models.BooleanField(
        default=False,
    )

    is_rejected = models.BooleanField(
        default=False,
    )

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self) -> str:
        return f'{self.text[:50]}...'

    def approve(self) -> None:
        self.is_approved = True
        self.save()

    def disapprove(self) -> None:
        self.is_approved = False
        self.save()

    def reject(self) -> None:
        self.is_rejected = True
        self.save()

    def unreject(self) -> None:
        self.is_rejected = False
        self.save()
