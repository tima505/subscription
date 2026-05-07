import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings_prod')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

# Delete existing user if exists
if User.objects.filter(username=username).exists():
    User.objects.filter(username=username).delete()
    print(f'Deleted existing user {username}')

# Create new superuser
user = User.objects.create_superuser(
    username=username,
    email=email,
    password=password,
    role='admin'
)
print(f'Superuser {username} created successfully with role admin!')
print(f'Username: {username}')
print(f'Password: {password}')

# Create manager user
manager_username = os.environ.get('DJANGO_MANAGER_USERNAME', 'manager')
manager_password = os.environ.get('DJANGO_MANAGER_PASSWORD', 'manager123')
manager_email = os.environ.get('DJANGO_MANAGER_EMAIL', 'manager@example.com')

if User.objects.filter(username=manager_username).exists():
    User.objects.filter(username=manager_username).delete()
    print(f'Deleted existing user {manager_username}')

manager = User.objects.create_user(
    username=manager_username,
    email=manager_email,
    password=manager_password,
    role='manager'
)
print(f'Manager {manager_username} created successfully!')
print(f'Username: {manager_username}')
print(f'Password: {manager_password}')
