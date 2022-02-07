from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError(_('TheGivenPhoneMustBeSet'))
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
                                 message=_("PhoneValidatorMessage"))
    phone = models.CharField(validators=[phone_regex], max_length=12, unique=True, verbose_name=_("PhoneNumber"),
                             blank=False, help_text=_("HelpTextPhone"))
    tg_id = models.IntegerField(null=True, blank=True, unique=True, verbose_name=_("TelegramID"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("DateOfBirth"))
    name = models.CharField(null=True, blank=True, max_length=100, verbose_name=_("Name"))
    email = models.EmailField(null=True, blank=True, verbose_name=_("Email"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
