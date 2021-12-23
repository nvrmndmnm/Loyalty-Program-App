from django.contrib.auth import get_user_model
from rest_framework import serializers
from merchantapp.models import Branch


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('phone', 'tg_id')


class BranchWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class BranchReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
