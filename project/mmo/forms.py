from django.forms import ModelForm, BooleanField  # true-false поле
from .models import Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class PostForm(ModelForm):
    check_box = BooleanField(label='Сохранить')
    class Meta:
        model = Post
        widgets = {
            'file': SummernoteWidget(),
        }
        fields = ['title', 'text', 'category', 'check_box', 'file']
        exclude = ["post_time", "author"]
