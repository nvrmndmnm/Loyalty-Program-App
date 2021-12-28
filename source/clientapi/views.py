import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from merchantapp.models import Branch, Order, UserReward
from clientapi.serializers import UserSerializer, BranchWriteSerializer, BranchReadSerializer, \
    ArticleWriteSerializer, ArticleReadSerializer, UserRewardWriteSerializer, UserRewardReadSerializer
from merchantapp.models import Branch, Article, UserReward, Program, ProgramCondition


class UserCreateAPIView(CreateAPIView, UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'phone'

    def get_object(self):
        try:
            return get_object_or_404(get_user_model(), phone=self.request.data['phone'])
        except:
            return None

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


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleWriteSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ArticleReadSerializer
        return self.serializer_class


class UserRewardViewSet(ModelViewSet):
    queryset = UserReward.objects.all()
    serializer_class = UserRewardWriteSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return UserRewardReadSerializer
        return self.serializer_class


@api_view(['GET'])
def get_user_progress(request, tg_id):
    user = get_object_or_404(get_user_model(), tg_id=tg_id)
    active_rewards = UserReward.objects.filter(user__phone=user.phone, redeemed=False).count()
    last_obtained_reward = UserReward.objects.filter(user__phone=user.phone).order_by('-time_created').first()
    last_orders_count = Order.objects.filter(user__phone=user.phone,
                                             status='FINISHED',
                                             program=1,
                                             completion_date__gt=last_obtained_reward.time_created
                                             if last_obtained_reward else datetime.datetime(1970, 1, 1)).count()
    required_orders = Program.objects.get(id=1).condition.amount
    return Response({"completed_orders": f"{last_orders_count}",
                     "program": f"{required_orders}",
                     "active_rewards": f"{active_rewards}"})
