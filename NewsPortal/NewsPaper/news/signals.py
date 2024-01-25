from datetime import datetime
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import PostCategory, Post, Author
from django.conf import settings

def send_notifications(preview, pk, title, subscribers):
    for subscriber in subscribers:
        html_content = render_to_string(
            'email_notification_message.html',
            {
                'username': subscriber.username,
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}'
            }
        )
        msg = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_users = []

        for ctg in categories:
            subscribers = ctg.subscribers.all()
            subscribers_users += [s for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_users)

@receiver(pre_save, sender=Post)
def check_for_saves(sender, instance, **kwargs):
    current_author = instance.author_id
    current_datetime = datetime.now()
    check = Post.objects.all().filter(author=Author.objects.get(id=current_author), published_date=current_datetime - datetime.timedelta(hours=24))
    if len(check) > 3:
        send_mail(
            subject='Внимание!',
            message='один пользователь не может публиковать более трех постов в сутки',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[Author.email]
        )
    raise Exception('Sorry, You can not post more than 3 posts per day')