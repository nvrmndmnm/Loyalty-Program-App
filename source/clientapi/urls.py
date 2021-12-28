from django.urls import path, include
from clientapi import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('branches', views.BranchViewSet)
router.register('articles', views.ArticleViewSet)
router.register('user_rewards', views.UserRewardViewSet)

app_name = 'clientapi'

urlpatterns = [
    path("", include(router.urls)),
    path('users/create/', views.UserCreateAPIView.as_view(),
         name='user-detail'),
    path('users/<int:tg_id>/progress/', views.get_user_progress, name='user_progress')
]
