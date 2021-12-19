from django.contrib.auth import get_user_model
from django.db import models

status_choices = [
    ('RETURNED', 'Возвращён'),
    ('FINISHED', 'Завершён')
]
merchant_categories = [
    ('CATERING', 'Кофейни, рестораны'),
    ('CAR', 'Обслуживание автомобиля')
]


class BaseModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name='Активировать')

    class Meta:
        abstract = True


class Merchant(BaseModel):
    code = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    director = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='merchant_director')
    category = models.CharField(choices=merchant_categories, max_length=20)

    def __str__(self):
        return f'{self.name}'


class Branch(BaseModel):
    code = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    merchant = models.ForeignKey('Merchant', on_delete=models.CASCADE, related_name='merchant')
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='address')
    description = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Address(BaseModel):
    street = models.CharField(max_length=150)
    building = models.CharField(max_length=20)
    apartment = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f'{self.street}'


class Program(BaseModel):
    code = models.CharField(max_length=150, unique=True, verbose_name='Код')
    title = models.CharField(max_length=150, verbose_name='Название')
    condition = models.ForeignKey('ProgramCondition', on_delete=models.CASCADE,
                                  related_name='condition', verbose_name='Условие')
    reward = models.ForeignKey('ProgramReward', on_delete=models.CASCADE, related_name='reward', verbose_name='Награда')
    branch = models.ManyToManyField('Branch', related_name='branch', verbose_name='Заведение')
    start_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')
    end_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата завершения')
    description = models.TextField(max_length=1000, verbose_name='Описание')

    def __str__(self):
        return self.title


class ProgramReward(BaseModel):
    reward_type = models.ForeignKey('ProgramRewardType', on_delete=models.CASCADE, related_name='type')
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{str(self.reward_type)} x {self.amount}"


class ProgramRewardType(BaseModel):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class ProgramCondition(BaseModel):
    condition_type = models.ForeignKey('ProgramConditionType', on_delete=models.CASCADE, related_name='type')
    amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{str(self.condition_type)} x {self.amount}"


class ProgramConditionType(BaseModel):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Order(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='order_user')
    status = models.CharField(choices=status_choices, max_length=50)
    completion_date = models.DateTimeField()
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='order_program')

    def __str__(self):
        return f'{self.pk}'


class UserReward(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_reward')
    program = models.ForeignKey('Program', on_delete=models.CASCADE, related_name='reward_program')
    expire_date = models.DateTimeField(blank=True, null=True)
    redeemed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.program.reward}'
