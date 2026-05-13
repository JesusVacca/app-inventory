from django.db.models.signals import post_migrate
from django.dispatch import receiver

from apps.accounts.models import Member


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if sender.name != 'apps.accounts': return
    email = 'apbautista@gmail.com'
    password = '1234567890'
    if not Member.objects.filter(email=email).exists():
        Member.objects.create_superuser(
            email=email,
            password=password,
            **{
                'first_name': 'Alexandra',
                'last_name':'Bautista',
                'phone_number':'3218194184'
            }
        )


