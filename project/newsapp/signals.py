from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory, Post
from django.conf import settings

from .tasks import new_post_subscription


def send_notifications(preview, pk, title, subscribers, id):
    mailing_list = list(PostCategory.objects.filter(postThrough_id=id).values_list(
            'categoryThrough__subscribers__username',
            'categoryThrough__subscribers__first_name',
            'categoryThrough__subscribers__email',
            'categoryThrough__name',
        )
    )

    for user, first_name, email, category in mailing_list:
        if not first_name:
            first_name = user

        html_content = render_to_string(
            'post_created_email.html',
            {
                'name': first_name,
                'category': category,
                'title': title,
                'text': preview,
                'link': f'{settings.SITE_URL}/news/{pk}',
            }
        )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    new_post_subscription(instance)
