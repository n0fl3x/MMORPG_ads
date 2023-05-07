from django.db import models


CATEGORIES = [
    ('TK', 'Tank'),
    ('HL', 'Healer'),
    ('DD', 'Damage dealer'),
    ('TR', 'Trader'),
    ('GM', 'Guild master'),
    ('QG', 'Quest giver'),
    ('WS', 'Warsmith'),
    ('TN', 'Tanner'),
    ('PM', 'Potion maker'),
    ('SM', 'Spell master'),
]


class Adv(models.Model):
    """Advertising representation class."""

    date_of_creation = models.DateTimeField(
        auto_now_add=True,
    )

    author = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='adv_created_by',
    )

    title = models.CharField(
        max_length=255,
        help_text='Up to 255 symbols',
    )

    category = models.CharField(
        max_length=2,
        choices=CATEGORIES,
        default=None,
    )

    content = models.TextField()

    class Meta:
        verbose_name = 'Advertise'
        verbose_name_plural = 'Advertisements'

    def __str__(self) -> str:
        return f'{self.title} by {self.author}'

    def get_adv_url(self) -> str:
        return f'ads/{self.id}/'


class Reply(models.Model):
    """Replies class for our advertisements."""

    date_of_creation = models.DateTimeField(
        auto_now_add=True,
    )

    author = models.ForeignKey(
        to='User',
        on_delete=models.CASCADE,
        related_name='reply_created_by',
    )

    adv = models.ForeignKey(
        to='Adv',
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
        return f'Reply #{self.id} by {self.author} to {self.adv}'

    def is_approved(self) -> None:
        self.approved = True
        self.save()
