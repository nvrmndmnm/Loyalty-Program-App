import factory
from django.contrib.auth import get_user_model
from merchantapp.models import Merchant
from accounts.models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()


class MerchantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Merchant


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
