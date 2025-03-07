from django.contrib import admin
from .models import CryptoWallet, Deposit, InvestmentPackage, Investment, Withdrawal, UserBalance

@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "network")

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "crypto_wallet", "status", "created_at")
    list_filter = ("status",)
    actions = ["confirm_deposit"]

    def confirm_deposit(self, request, queryset):
        for deposit in queryset.filter(status="Pending"):
            deposit.status = "Confirmed"
            deposit.save()
            user_balance = UserBalance.objects.get(user=deposit.user)
            user_balance.balance += deposit.amount
            user_balance.save()
        self.message_user(request, "Selected deposits confirmed and user balance updated.")

@admin.register(InvestmentPackage)
class InvestmentPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "min_amount", "weekly_profit_percent")

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ("user", "package", "amount", "status", "start_date", "next_payout_date")

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "crypto_address", "status", "created_at")
    list_filter = ("status",)
    actions = ["approve_withdrawal"]

    def approve_withdrawal(self, request, queryset):
        for withdrawal in queryset.filter(status="Pending"):
            user_balance = UserBalance.objects.get(user=withdrawal.user)
            if user_balance.balance >= withdrawal.amount:
                withdrawal.status = "Approved"
                user_balance.balance -= withdrawal.amount
                user_balance.save()
                withdrawal.save()
                self.message_user(request, "Selected withdrawals approved.")
            else:
                self.message_user(request, "Insufficient balance for selected withdrawals.", level="error")

@admin.register(UserBalance)
class UserBalanceAdmin(admin.ModelAdmin):
    list_display = ("user", "balance")
    