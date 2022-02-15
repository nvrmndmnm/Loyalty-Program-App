from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _


status_choices = [
    ('RETURNED', _('Returned')),
    ('FINISHED', _('Finished'))
]
merchant_categories = [
    ('CATERING', _('Catering')),
    ('CAR', _('Car'))
]


class BaseModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True, verbose_name=_('TimeCreated'))
    time_updated = models.DateTimeField(auto_now=True, verbose_name=_('TimeUpdated'))
    active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        abstract = True


class Merchant(BaseModel):
    code = models.CharField(max_length=150, unique=True, verbose_name=_('Identifier'))
    name = models.CharField(max_length=150, verbose_name=_('Title'))
    director = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 related_name='merchant_director', verbose_name=_('Supervisor'))
    employees = models.ManyToManyField(get_user_model(), related_name='merchants', verbose_name=_('Employees'))
    category = models.CharField(choices=merchant_categories, max_length=20, verbose_name=_('Category'))

    def __str__(self):
        return f'{self.name}'


class Branch(BaseModel):
    code = models.CharField(max_length=150, unique=True, verbose_name=_('Identifier'))
    name = models.CharField(max_length=150, verbose_name=_('Title'))
    merchant = models.ForeignKey('Merchant', on_delete=models.CASCADE, related_name='merchant', verbose_name=_('Partner'))
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='address', verbose_name='Адрес')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name=_('Description'))

    def __str__(self):
        return f'{self.name}'


class Address(BaseModel):
    street = models.CharField(max_length=150, verbose_name=_('Street'))
    building = models.CharField(max_length=20, verbose_name=_('Building'))
    apartment = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Office'))
    city = models.CharField(max_length=50, verbose_name=_('City'))
    link2gis = models.URLField(verbose_name=_('LinkTo2GIS'))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('Latitude'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('Longitude'))

    def __str__(self):
        return f'{self.street}'


class Program(BaseModel):
    code = models.CharField(max_length=150, unique=True, verbose_name=_('Identifier'))
    title = models.CharField(max_length=150, verbose_name=_('Title'))
    condition = models.ForeignKey('ProgramCondition', on_delete=models.CASCADE,
                                  related_name='condition', verbose_name=_('Condition'))
    reward = models.ForeignKey('ProgramReward', on_delete=models.CASCADE, related_name='reward', verbose_name=_('Reward'))
    branch = models.ManyToManyField('Branch', related_name='branch', verbose_name=_('Branch'))
    start_date = models.DateTimeField(blank=True, null=True, verbose_name=_('StartDate'))
    end_date = models.DateTimeField(blank=True, null=True, verbose_name=_('EndDate'))
    description = models.TextField(max_length=1000, verbose_name=_('Description'))

    def __str__(self):
        return self.title


class ProgramReward(BaseModel):
    reward_type = models.ForeignKey('ProgramRewardType', on_delete=models.CASCADE,
                                    related_name='type', verbose_name=_('RewardType'))
    amount = models.PositiveIntegerField(default=0, verbose_name=_('Amount'))

    def __str__(self):
        return f"{str(self.reward_type)} x {self.amount}"


class ProgramRewardType(BaseModel):
    code = models.CharField(max_length=50, verbose_name=_('Identifier'))
    title = models.CharField(max_length=150, verbose_name=_('Title'))

    def __str__(self):
        return self.title


class ProgramCondition(BaseModel):
    condition_type = models.ForeignKey('ProgramConditionType', on_delete=models.CASCADE,
                                       related_name='type', verbose_name=_('ConditionType'))
    amount = models.PositiveIntegerField(default=0, verbose_name=_('Amount'))

    def __str__(self):
        return f"{str(self.condition_type)} x {self.amount}"


class ProgramConditionType(BaseModel):
    code = models.CharField(max_length=50, verbose_name=_('Identifier'))
    title = models.CharField(max_length=150, verbose_name=_('Title'))

    def __str__(self):
        return self.title


class Order(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='order_user', verbose_name=_('User'))
    status = models.CharField(choices=status_choices, max_length=50, verbose_name=_('Status'))
    completion_date = models.DateTimeField(verbose_name=_('EndDate'))
    amount = models.PositiveIntegerField(verbose_name=_('Amount'))
    price = models.PositiveIntegerField(verbose_name=_('Price'))
    program = models.ForeignKey('Program', on_delete=models.CASCADE,
                                related_name='order_program', verbose_name=_('Program'))

    def __str__(self):
        return f'{self.pk} - {self.user}'


class UserReward(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='user_reward', verbose_name=_('User'))
    program = models.ForeignKey('Program', on_delete=models.CASCADE,
                                related_name='reward_program', verbose_name=_('Program'))
    expire_date = models.DateTimeField(blank=True, null=True, verbose_name=_('ExpireDate'))
    redeemed = models.BooleanField(default=False, verbose_name=_('Redeemed'))

    def __str__(self):
        return f'{self.user} - {self.program.reward}'


class Article(BaseModel):
    title = models.CharField(max_length=150, verbose_name=_('TitleZ'))
    text = models.TextField(max_length=2000, verbose_name=_('Text'))
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               related_name='article_author', verbose_name=_('Author'))

    def __str__(self):
        return f'{self.title} - {self.author}'
