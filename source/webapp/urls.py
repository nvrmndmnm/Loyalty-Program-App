from django.urls import path
from webapp import views

app_name = 'webapp'

urlpatterns = [
    path('', views.index_view, name='index'),
]
