from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from companies.models import Company, Share


@receiver(post_save, sender=Company)
def distribute_shares(sender, instance, created, **kwargs):
    if created:
        users = User.objects.all()
        if not users.exists():
            return

        shares_per_user = instance.total_shares // users.count()
        for user in users:
            Share.objects.create(
                owner=user,
                company=instance,
                quantity=shares_per_user
            )
