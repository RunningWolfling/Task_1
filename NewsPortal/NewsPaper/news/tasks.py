import datetime

from celery import shared_task
from .models import Post, Category, PostCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone

@shared_task
def added_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    head = post.head
    preview = post.preview()
    subscribers_email = []

    for ctg in categories:
        subscribers = ctg.subscribers.all()
        subscribers_email += [s.email for s in subscribers]

        html_content = render_to_string(
            'email_notification_message.html',
            {
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}'
            }
        )

        msg = EmailMultiAlternatives(
            subject=head,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

@shared_task
def notification_every_week():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_date__gt=last_week)
    catigories = set(posts.values_list('catigories__catigory_name', flat=True))
    subscribers = set(Category.objects.filter(catigory_name__in=catigories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Новое за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()