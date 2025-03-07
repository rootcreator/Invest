from celery import shared_task
from django.db import transaction
from .models import Investment, UserBalance
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@shared_task
def calculate_weekly_profits():
    """Calculates and distributes weekly profits to active investments."""
    investments = Investment.objects.filter(status="Active")

    if not investments.exists():
        logger.info("No active investments found. Skipping weekly profit calculation.")
        return

    updated_balances = []

    with transaction.atomic():
        for investment in investments:
            try:
                weekly_profit = (investment.amount * investment.package.weekly_profit_percent) / 100
                user_balance, created = UserBalance.objects.get_or_create(user=investment.user)

                user_balance.balance += weekly_profit
                updated_balances.append(user_balance)

                logger.info(f"Added ${weekly_profit:.2f} weekly profit to {investment.user.username}'s account.")

            except Exception as e:
                logger.error(f"Error processing investment {investment.id}: {e}")

        # Bulk update balances for efficiency
        UserBalance.objects.bulk_update(updated_balances, ["balance"])

    logger.info("Weekly profit calculation completed successfully.")


@shared_task
def calculate_monthly_profits():
    """Calculates and distributes monthly profits to active investments (runs only on the first day of each month)."""
    today = datetime.today()

    # Only run on the 1st of the month
    if today.day != 1:
        logger.info("Skipping monthly profit calculation as today is not the 1st of the month.")
        return

    investments = Investment.objects.filter(status="Active")

    if not investments.exists():
        logger.info("No active investments found. Skipping monthly profit calculation.")
        return

    updated_balances = []

    with transaction.atomic():
        for investment in investments:
            try:
                monthly_profit = (investment.amount * investment.package.monthly_profit_percent) / 100
                user_balance, created = UserBalance.objects.get_or_create(user=investment.user)

                user_balance.balance += monthly_profit
                updated_balances.append(user_balance)

                logger.info(f"Added ${monthly_profit:.2f} monthly profit to {investment.user.username}'s account.")

            except Exception as e:
                logger.error(f"Error processing investment {investment.id}: {e}")

        # Bulk update balances for efficiency
        UserBalance.objects.bulk_update(updated_balances, ["balance"])

    logger.info("Monthly profit calculation completed successfully.")
