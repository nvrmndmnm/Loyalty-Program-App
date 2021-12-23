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
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    active = models.BooleanField(default=True, verbose_name='Активировать')

    class Meta:
        abstract = True


class Merchant(BaseModel):
    code = models.CharField(max_length=150, unique=True, verbose_name='Идентификатор')
    name = models.CharField(max_length=150, verbose_name='Название')
    director = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 related_name='merchant_director', verbose_name='Руководитель')
    category = models.CharField(choices=merchant_categories, max_length=20, verbose_name='Категория')

    def __str__(self):
        return f'{self.name}'


class Branch(BaseModel):
    code = models.CharField(max_length=150, unique=True, verbose_name='Идентификатор')
    name = models.CharField(max_length=150, verbose_name='Название')
    merchant = models.ForeignKey('Merchant', on_delete=models.CASCADE, related_name='merchant', verbose_name='Партнёр')
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='address', verbose_name='Адрес')
    description = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'


class Address(BaseModel):
    street = models.CharField(max_length=150, verbose_name='Улица')
    building = models.CharField(max_length=20, verbose_name='Здание')
    apartment = models.CharField(max_length=20, blank=True, null=True, verbose_name='Офис')
    city = models.CharField(max_length=50, verbose_name='Город')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Долгота')

    def __str__(self):
        return f'{self.street}'


class Program(BaseModel):
    code = models.CharField(max_length=150, unique=True, verbose_name='Идентификатор')
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
    reward_type = models.ForeignKey('ProgramRewardType', on_delete=models.CASCADE,
                                    related_name='type', verbose_name='Тип награды')
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f"{str(self.reward_type)} x {self.amount}"


class ProgramRewardType(BaseModel):
    code = models.CharField(max_length=50, verbose_name='Идентификатор')
    title = models.CharField(max_length=150, verbose_name='Название')

    def __str__(self):
        return self.title


class ProgramCondition(BaseModel):
    condition_type = models.ForeignKey('ProgramConditionType', on_delete=models.CASCADE,
                                       related_name='type', verbose_name='Тип условия')
    amount = models.PositiveIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f"{str(self.condition_type)} x {self.amount}"


class ProgramConditionType(BaseModel):
    code = models.CharField(max_length=50, verbose_name='Идентификатор')
    title = models.CharField(max_length=150, verbose_name='Название')

    def __str__(self):
        return self.title


class Order(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='order_user', verbose_name='Пользователь')
    status = models.CharField(choices=status_choices, max_length=50, verbose_name='Статус')
    completion_date = models.DateTimeField(verbose_name='Дата завершения')
    amount = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    program = models.ForeignKey('Program', on_delete=models.CASCADE,
                                related_name='order_program', verbose_name='Программа')

    def __str__(self):
        return f'{self.pk} - {self.user}'


class UserReward(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='user_reward', verbose_name='Пользователь')
    program = models.ForeignKey('Program', on_delete=models.CASCADE,
                                related_name='reward_program', verbose_name='Программа')
    expire_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата истечения')
    redeemed = models.BooleanField(default=False, verbose_name='Выдан')

    def __str__(self):
        return f'{self.user} - {self.program.reward}'


class Article(BaseModel):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    text = models.TextField(max_length=2000, verbose_name='Текст')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                               related_name='article_author', verbose_name='Автор')

    def __str__(self):
        return f'{self.title} - {self.author}'
