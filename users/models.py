from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.staticfiles.storage import staticfiles_storage

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Удаляем поле username
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='Страна')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    verification_token = models.CharField(max_length=100, blank=True, null=True, verbose_name='Токен')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Убираем 'email' из REQUIRED_FIELDS

    objects = CustomUserManager()  # Подключаем кастомный менеджер

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return staticfiles_storage.url('img/default-avatar.png')
