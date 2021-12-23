from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from clientapi.serializers import UserSerializer, BranchWriteSerializer, BranchReadSerializer
from merchantapp.models import Branch


class UserCreateAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'phone'


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchWriteSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BranchReadSerializer
        return self.serializer_class
