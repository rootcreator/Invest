from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse, BadHeaderError, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import TemplateView
from decimal import Decimal
from .models import CryptoWallet, Deposit
from .models import Investment, InvestmentPackage, Withdrawal, UserBalance


def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        email = request.POST.get("email").strip()
        password = request.POST.get("password").strip()
        confirm_password = request.POST.get("confirm_password").strip()

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "register.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create an initial UserBalance entry
        UserBalance.objects.create(user=user, balance=0.0)

        # Log in the user after successful registration
        login(request, user)
        return redirect("dashboard")

    return render(request, "register.html")

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Create this template

def csrf_token_view(request):
    return JsonResponse({"csrfToken": get_token(request)})

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Your Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'noreply@yourwebsite.com',
                                 [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
            messages.error(request, "An invalid email has been entered.")
    password_reset_form = PasswordResetForm()
    return render(request=request,
                  template_name="password_reset.html",
                  context={"form": password_reset_form})

# Dashboard View (Shows balance, investments, notifications)
@login_required
def dashboard(request):
    user_balance = UserBalance.objects.get(user=request.user)
    investments = Investment.objects.filter(user=request.user)
    withdrawals = Withdrawal.objects.filter(user=request.user)
    deposits = Deposit.objects.filter(user=request.user)

    context = {
        "balance": user_balance.balance,
        "investments": investments,
        "withdrawals": withdrawals,
        "deposits": deposits,
        "notifications": ["Your latest deposit is pending approval.", "Weekly profit payout scheduled."]
    }
    return render(request, "dashboard.html", context)

# Deposit Page
@login_required
def deposit_page(request):
    wallets = CryptoWallet.objects.all()

    if request.method == "POST":
        amount = request.POST["amount"]
        wallet_id = request.POST["crypto_wallet"]
        transaction_id = request.POST["transaction_id"]  # User enters transaction hash/ID

        wallet = get_object_or_404(CryptoWallet, id=wallet_id)

        # Create a pending deposit entry
        deposit = Deposit.objects.create(
            user=request.user,
            amount=amount,
            crypto_wallet=wallet,
            transaction_id=transaction_id,
            status="Pending"
        )

        messages.success(request, "Deposit request submitted. Awaiting confirmation.")
        return redirect("dashboard")

    return render(request, "deposit.html", {"wallets": wallets})

# Investment Page
@login_required
def invest_page(request):
    packages = InvestmentPackage.objects.filter(status="Active")  # Only active packages

    if request.method == "POST":
        package_id = request.POST.get("package_id")
        amount = request.POST.get("amount")

        try:
            package = get_object_or_404(InvestmentPackage, id=package_id)
            user_balance = UserBalance.objects.get(user=request.user)
            amount = float(amount)

            if amount < package.min_amount:
                messages.error(request, f"Minimum investment for {package.name} is ${package.min_amount}.")
            elif user_balance.balance < amount:
                messages.error(request, "Insufficient balance.")
            else:
                # Check if user already has an active investment in this package
                existing_investment = Investment.objects.filter(user=request.user, package=package, status="Active").exists()
                if existing_investment:
                    messages.error(request, "You already have an active investment in this package.")
                else:
                    Investment.objects.create(user=request.user, package=package, amount=amount, status="Active")
                    user_balance.balance -= Decimal(amount)
                    user_balance.save()

                    messages.success(request, f"Investment of ${amount} in {package.name} successful!")
                    return redirect("dashboard")

        except ValueError:
            messages.error(request, "Invalid amount entered.")

    return render(request, "invest.html", {"packages": packages})

# Withdrawal Page
@login_required
def withdraw_page(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        address = request.POST["crypto_address"]
        user_balance = UserBalance.objects.get(user=request.user)

        if user_balance.balance >= float(amount):
            Withdrawal.objects.create(user=request.user, amount=amount, crypto_address=address, status="Pending")
            return redirect("dashboard")
        else:
            return render(request, "withdraw.html", {"error": "Insufficient balance."})

    return render(request, "withdraw.html")

# Home Page (Landing Page)
class HomePageView(TemplateView):
    template_name = "index.html"