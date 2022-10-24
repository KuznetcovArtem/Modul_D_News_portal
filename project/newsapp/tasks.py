from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, PostCategory


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    notify_subscribers_for_new_post.apply_async(
        (instance.id, instance.title, instance.text),
        countdown=10,
    )


@shared_task
def notify_subscribers_for_new_post(id, title, text):
    print(PostCategory.objects.filter(postThrough_id=id))
