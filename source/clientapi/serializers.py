from rest_framework import serializers
from merchantapp.models import Branch


class BranchWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class BranchReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
