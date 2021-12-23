from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    phone_regex = RegexValidator(regex=r'^7?\d{10}',
                                 message="Phone number must be entered in the format: '+77071234567'")
    phone = models.CharField(validators=[phone_regex], max_length=12, unique=True, verbose_name='Номер телефона',
                             blank=False, help_text='Enter 10 digits phone number with +7')
    tg_id = models.IntegerField(null=True, blank=True, unique=True, verbose_name='Telegram ID')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    name = models.CharField(null=True, blank=True, max_length=100, verbose_name='Имя')
    email = models.EmailField(null=True, blank=True, verbose_name="Email")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
