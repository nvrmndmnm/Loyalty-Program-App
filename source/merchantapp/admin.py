from django.contrib import admin
from merchantapp.models import Merchant, Branch, Address, Program, ProgramCondition,\
    ProgramReward, ProgramConditionType, ProgramRewardType, Order, UserReward, Article

admin.site.register(Merchant)
admin.site.register(Branch)
admin.site.register(Address)
admin.site.register(Program)
admin.site.register(ProgramCondition)
admin.site.register(ProgramReward)
admin.site.register(ProgramConditionType)
admin.site.register(ProgramRewardType)
admin.site.register(Order)
admin.site.register(UserReward)
admin.site.register(Article)
