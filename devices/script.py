from django.contrib.auth.models import User
from .models import Profile  # Замените на ваш путь к модели Profile

# Найдите всех пользователей, у которых нет профиля
for user in User.objects.filter(profile__isnull=True):
    # Создайте профиль для каждого пользователя
    Profile.objects.create(user=user)
    print(f"Profile created for user: {user.username}")
