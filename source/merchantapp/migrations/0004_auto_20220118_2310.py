# Generated by Django 3.2 on 2022-01-18 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchantapp', '0003_address_link2gis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='address',
            name='apartment',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Office'),
        ),
        migrations.AlterField(
            model_name='address',
            name='building',
            field=models.CharField(max_length=20, verbose_name='Building'),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=50, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='address',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='address',
            name='link2gis',
            field=models.URLField(verbose_name='LinkTo2GIS'),
        ),
        migrations.AlterField(
            model_name='address',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=150, verbose_name='Street'),
        ),
        migrations.AlterField(
            model_name='address',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='address',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='article',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_author', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='article',
            name='text',
            field=models.TextField(max_length=2000, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='article',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='article',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=150, verbose_name='TitleZ'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='code',
            field=models.CharField(max_length=150, unique=True, verbose_name='Identifier'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchant', to='merchantapp.merchant', verbose_name='Partner'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='category',
            field=models.CharField(choices=[('CATERING', 'Catering'), ('CAR', 'Car')], max_length=20, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='code',
            field=models.CharField(max_length=150, unique=True, verbose_name='Identifier'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='director',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='merchant_director', to=settings.AUTH_USER_MODEL, verbose_name='Supervisor'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='order',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='order',
            name='completion_date',
            field=models.DateTimeField(verbose_name='EndDate'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='order',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_program', to='merchantapp.program', verbose_name='Program'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('RETURNED', 'Returned'), ('FINISHED', 'Finished')], max_length=50, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='order',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='program',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='program',
            name='branch',
            field=models.ManyToManyField(related_name='branch', to='merchantapp.Branch', verbose_name='Branch'),
        ),
        migrations.AlterField(
            model_name='program',
            name='code',
            field=models.CharField(max_length=150, unique=True, verbose_name='Identifier'),
        ),
        migrations.AlterField(
            model_name='program',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='condition', to='merchantapp.programcondition', verbose_name='Condition'),
        ),
        migrations.AlterField(
            model_name='program',
            name='description',
            field=models.TextField(max_length=1000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='program',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='EndDate'),
        ),
        migrations.AlterField(
            model_name='program',
            name='reward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reward', to='merchantapp.programreward', verbose_name='Reward'),
        ),
        migrations.AlterField(
            model_name='program',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='StartDate'),
        ),
        migrations.AlterField(
            model_name='program',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='program',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='program',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='programcondition',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='programcondition',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='programcondition',
            name='condition_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type', to='merchantapp.programconditiontype', verbose_name='ConditionType'),
        ),
        migrations.AlterField(
            model_name='programcondition',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='programcondition',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='programconditiontype',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='programconditiontype',
            name='code',
            field=models.CharField(max_length=50, verbose_name='Identifier'),
        ),
        migrations.AlterField(
            model_name='programconditiontype',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='programconditiontype',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='programconditiontype',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='programreward',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='programreward',
            name='amount',
            field=models.PositiveIntegerField(default=0, verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='programreward',
            name='reward_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type', to='merchantapp.programrewardtype', verbose_name='RewardType'),
        ),
        migrations.AlterField(
            model_name='programreward',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='programreward',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='programrewardtype',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='programrewardtype',
            name='code',
            field=models.CharField(max_length=50, verbose_name='Identifier'),
        ),
        migrations.AlterField(
            model_name='programrewardtype',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='programrewardtype',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='programrewardtype',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='userreward',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
        migrations.AlterField(
            model_name='userreward',
            name='expire_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='ExpireDate'),
        ),
        migrations.AlterField(
            model_name='userreward',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reward_program', to='merchantapp.program', verbose_name='Program'),
        ),
        migrations.AlterField(
            model_name='userreward',
            name='redeemed',
            field=models.BooleanField(default=False, verbose_name='Redeemed'),
        ),
        migrations.AlterField(
            model_name='userreward',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='TimeCreated'),
        ),
        migrations.AlterField(
            model_name='userreward',
            name='time_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='TimeUpdated'),
        ),
        migrations.AlterField(
            model_name='userreward',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reward', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
