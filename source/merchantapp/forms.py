from django import forms

from merchantapp.models import Program, ProgramCondition, ProgramConditionType, ProgramReward, ProgramRewardType,\
    Branch, Address


class UserSearchForm(forms.Form):
    id = forms.CharField(max_length=150, required=False, label='Search')


class ProgramForm(forms.ModelForm):
    condition = forms.IntegerField(min_value=0, label='Требуется покупок')
    reward = forms.IntegerField(min_value=0, label='Будет начислено наград')

    def clean(self):
        cleaned_data = super().clean()

        default_program_condition_type = 'number_of_purchases'
        condition_type = ProgramConditionType.objects.get(code__exact=default_program_condition_type)
        condition = ProgramCondition.objects.get_or_create(condition_type=condition_type,
                                                           amount=cleaned_data['condition'])
        default_program_reward_type = 'free_product'
        reward_type = ProgramRewardType.objects.get(code__exact=default_program_reward_type)
        reward = ProgramReward.objects.get_or_create(reward_type=reward_type,
                                                     amount=cleaned_data['reward'])

        cleaned_data['condition'] = condition[0]
        cleaned_data['reward'] = reward[0]

        return cleaned_data

    class Meta:
        model = Program
        fields = ['code', 'title', 'condition', 'reward', 'branch', 'description', 'active']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['active']


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['code', 'name', 'merchant', 'description', 'active']
