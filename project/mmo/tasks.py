import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


# Реализовать рассылку уведомлений подписчикам после создания новости.
@shared_task
def info_after_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.title
    suscribers_emails = []

    for category in categories:
        suscribers_users = category.subscribers.all()
        for sub_users in suscribers_users:
            suscribers_emails.append(sub_users.email)

    html_content = render_to_string(
        'send/post_created_email.html',
        {
            'text': f'{post.title}',
            'link': f'{settings.SITE_URL}/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=suscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# Реализовать еженедельную рассылку с последними новостями (каждый понедельник в 8:00 утра)
@shared_task
def weekly_send_news():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts_per_week = Post.objects.filter(post_time__gte=last_week)
    subscribers = set(Post.author.objects.all().values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'weekly_posts.html',
        {
            'link': settings.SITE_URL,
            'posts_per_week': posts_per_week,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новые статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

    print(f'Emails sent to: {subscribers}')
