from django.contrib.auth import get_user_model
from rest_framework import serializers
from merchantapp.models import Branch, Article , UserReward


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('phone', 'tg_id', 'first_name', 'last_name')


class BranchWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class BranchReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ["name", "address", "description"]


class ArticleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class ArticleReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["time_created","title", "text"]


class UserRewardWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReward
        fields = "__all__"


class UserRewardReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReward
        fields = "__all__"
