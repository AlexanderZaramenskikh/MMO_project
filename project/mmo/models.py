from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

CATEGORY = [('Танки', 'Танки'), ('Хилы', 'Хилы',), ('ДД', 'ДД'), ('Торговцы', 'Торговцы'),
            ('Гилдмастеры', 'Гилдмастеры'), ('Квестгиверы', 'Квестгиверы'), ('Кузнецы', 'Кузнецы,'),
            ('Кожевники', 'Кожевники'), ('Зельевары', 'Зельевары'), ('Мастера заклинаний', 'Мастера заклинаний')]


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text=_("Автор"))
    nickname = models.CharField(max_length=100, help_text=_("Никнейм"))

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text=_("Автор"))
    post_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(_('Заголовок'), max_length=100, help_text=_("Введите заголовок"))
    text = models.TextField(_('Содержание'), help_text=_("Содержание статьи"))
    file = models.CharField(max_length=50000)
    category = models.CharField(_('Категория'), max_length=20, choices=CATEGORY, help_text=_('Введите категорию'))

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return f'/news/{self.id}'


class Comment(models.Model):
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Отклик от автора {self.user}: {self.text}"
