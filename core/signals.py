from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Deposit, UserBalance

@receiver(post_save, sender=Deposit)
def update_user_balance(sender, instance, **kwargs):
    """
    Update user's balance when a deposit is confirmed.
    """
    if instance.status == "Confirmed":
        user_balance, created = UserBalance.objects.get_or_create(user=instance.user)
        user_balance.balance += instance.amount
        user_balance.save()
