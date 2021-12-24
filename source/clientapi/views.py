import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from clientapi.serializers import UserSerializer, BranchWriteSerializer, BranchReadSerializer
from merchantapp.models import Branch, Order, UserReward


class UserCreateAPIView(CreateAPIView, UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'phone'

    def get_object(self):
        return get_object_or_404(get_user_model(), phone=self.request.data['phone'])

    def post(self, request, *args, **kwargs):
        customer = self.get_object()
        if customer:
            return self.update(request, *args, **kwargs)
        else:
            return self.create(request, *args, **kwargs)


class BranchViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchWriteSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return BranchReadSerializer
        return self.serializer_class


@api_view(['GET'])
def get_user_progress(request, phone):
    last_obtained_reward = UserReward.objects.filter(user__phone=phone).order_by('-time_created').first()
    last_orders_count = Order.objects.filter(user__phone=phone,
                                             status='FINISHED',
                                             program=1,
                                             completion_date__gt=last_obtained_reward.time_created
                                             if last_obtained_reward else datetime.datetime(1970, 1, 1)).count()
    return Response({"message": f"{last_orders_count}"})
