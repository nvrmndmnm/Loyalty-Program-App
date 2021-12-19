from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from clientapi.serializers import BranchWriteSerializer, BranchReadSerializer
from merchantapp.models import Branch


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchWriteSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BranchReadSerializer
        return self.serializer_class
