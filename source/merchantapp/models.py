from django.contrib.auth import get_user_model
from django.db import models

status_choices = [
    ('RETURNED', 'Returned'),
    ('FINISHED', 'Finished')
]


class BaseModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Merchant(BaseModel):
    name = models.CharField(max_length=150)


class Branch(BaseModel):
    name = models.CharField(max_length=150)
    merchant = models.ForeignKey('Merchant', on_delete=models.CASCADE, related_name='merchant')
    address = models.ForeignKey('Address', on_delete=models.CASCADE, related_name='address')

    def __str__(self):
        return f'{self.name}'


class Address(BaseModel):
    street = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.street}'


class Program(BaseModel):
    title = models.CharField(max_length=150)
    condition = models.ForeignKey('ProgramCondition', on_delete=models.CASCADE, related_name='condition')
    reward = models.ForeignKey('ProgramReward', on_delete=models.CASCADE, related_name='reward')
    branch = models.ManyToManyField('Branch', related_name='branch')
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.title


class ProgramReward(BaseModel):
    reward_type = models.ForeignKey('ProgramRewardType', on_delete=models.CASCADE, related_name='type')
    size = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{str(self.reward_type)} x {self.size}"


class ProgramRewardType(BaseModel):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class ProgramCondition(BaseModel):
    condition_type = models.ForeignKey('ProgramConditionType', on_delete=models.CASCADE, related_name='type')
    size = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{str(self.condition_type)} x {self.size}"


class ProgramConditionType(BaseModel):
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

    def get_redeemable(self):
        print('oalek')
        return UserReward.objects.filter(redeemed=False)

    def __str__(self):
        return f'{self.user} - {self.program.reward}'
