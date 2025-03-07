import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "investment.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
admin_username = os.getenv("ADMIN_USERNAME", "admin")
admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
admin_password = os.getenv("ADMIN_PASSWORD", "securepassword")

if not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(admin_username, admin_email, admin_password)
    print(f"Admin user '{admin_username}' created successfully.")
else:
    print(f"Admin user '{admin_username}' already exists.")
