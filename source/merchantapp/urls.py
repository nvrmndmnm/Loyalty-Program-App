from django.urls import path
from merchantapp import views as merchant_views

app_name = 'merchantapp'

urlpatterns = [
    path('', merchant_views.MerchantIndexView.as_view(), name='merchant_index'),
    path('s/', merchant_views.CustomerSearchView.as_view(), name='user_search'),
    path('customers/', merchant_views.CustomerListView.as_view(), name='customers'),
    path('customers/download/', merchant_views.download_customers_file, name='customers_download'),
    path('programs/', merchant_views.ProgramListView.as_view(), name='programs'),
    path('programs/create/', merchant_views.ProgramCreateView.as_view(), name='program_create'),
    path('programs/<int:pk>/update/', merchant_views.ProgramUpdateView.as_view(), name='program_update'),
    path('branches/', merchant_views.BranchListView.as_view(), name='branches'),
    path('branches/create/', merchant_views.BranchCreateView.as_view(), name='branch_create'),
    path('branches/<int:pk>/update/', merchant_views.BranchUpdateView.as_view(), name='branch_update'),
    path('orders/<int:pk>/', merchant_views.OrderProcessingView.as_view(), name='orders'),
    path('orders/create/', merchant_views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/redeem/', merchant_views.redeem_user_reward, name='redeem_user_reward')
]
