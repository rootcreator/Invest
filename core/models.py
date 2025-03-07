from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Crypto Wallet Model (Admin-Managable)
class CryptoWallet(models.Model):
    name = models.CharField(max_length=100)  # e.g., Bitcoin, Ethereum
    address = models.CharField(max_length=255)  
    network = models.CharField(max_length=50, choices=[("BTC", "Bitcoin"), ("ETH", "Ethereum"), ("BSC", "Binance Smart Chain"), ("USDT", "USDT")])

    def __str__(self):
        return f"{self.name} ({self.network})"

# Deposit Model
class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    crypto_wallet = models.ForeignKey(CryptoWallet, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, unique=True)  # User enters transaction hash
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Confirmed", "Confirmed"), ("Rejected", "Rejected")],
        default="Pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.status}"


# Investment Package Model
class InvestmentPackage(models.Model):
    RISK_LEVEL_CHOICES = [
        ("Low", "Low Risk"),
        ("Medium", "Medium Risk"),
        ("High", "High Risk"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, help_text="Brief details about this investment package.")
    min_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Minimum amount required to invest.")
    duration_weeks = models.PositiveIntegerField(default=4, help_text="Minimum duration for this investment (in weeks).")
    weekly_profit_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Expected weekly return as a percentage.")
    monthly_profit_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text="Expected monthly return as a percentage.")
    risk_level = models.CharField(max_length=10, choices=RISK_LEVEL_CHOICES, default="Medium")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Active")

    created_at = models.DateTimeField(default=now)  # Set default
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} | Min: ${self.min_amount} | {self.weekly_profit_percent}% Weekly | Risk: {self.risk_level}"

    class Meta:
        ordering = ["min_amount"]
        verbose_name = "Investment Package"
        verbose_name_plural = "Investment Packages"


# Investment Model
class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(InvestmentPackage, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("Active", "Active"), ("Completed", "Completed")], default="Active")
    start_date = models.DateTimeField(default=now)
    next_payout_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.package.name} - ${self.amount}"

# Withdrawal Model
class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    crypto_address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")], default="Pending")
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} ({self.status})"

# User Balance Model
class UserBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} - ${self.balance}"
        