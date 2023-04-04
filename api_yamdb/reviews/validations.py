from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Review


@receiver(pre_save, sender=Review)
def limit_reviews_per_author(sender, instance, **kwargs):
    max_reviews_per_author = 1
    existing_reviews = Review.objects.filter(
        author=instance.author, title=instance.title
    )

    if existing_reviews.count() >= max_reviews_per_author:
        return Response(status=status.HTTP_400_BAD_REQUEST)
