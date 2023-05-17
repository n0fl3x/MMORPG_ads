from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import ModelForm, ChoiceField, CharField

from .models import Adv, CATEGORIES


class AdvForm(ModelForm):
    category = ChoiceField(
        choices=CATEGORIES,
        label='Select category',
        help_text='Required field.',
        error_messages={
            'required': 'You need to select one category!',
        }
    )

    title = CharField(
        min_length=1,
        label='Title',
        help_text='Required field. At least 1 symbol.',
        error_messages={
            'required': 'You need to add something!',
        }
    )

    content = CharField(
        widget=CKEditorUploadingWidget(),
        label='Content of ad',
        required=False,
        help_text='Could be empty.',
    )

    class Meta:
        model = Adv
        fields = [
            'category',
            'title',
            'content',
        ]
