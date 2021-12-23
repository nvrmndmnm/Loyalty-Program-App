from django.urls import path, include
from clientapi import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('branches', views.BranchViewSet)

app_name = 'clientapi'

urlpatterns = [
    path("", include(router.urls)),
    path('users/create/', views.UserCreateAPIView.as_view(),
         name='user-detail')
]
