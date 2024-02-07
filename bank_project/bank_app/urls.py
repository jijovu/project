
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('home/', views.home,name='home'),
    path('account_open/', views.account_open,name='account_open'),
    path('account/<int:id>', views.account,name='account'),
    path('login/', views.signin,name='login'),
    path('deposit/<int:id>', views.deposit,name='deposit'),
    path('withdraw/<int:id>', views.withdraw,name='withdraw'),
    path('edit_login/', views.edit_login,name='edit_login'),
    path('edit_profile/<int:id>', views.edit_profile,name='edit_profile'),
    path('transaction/<int:id>', views.transaction,name='transaction'),
    path('admin_login/', views.admin_login,name='admin_login'),
    path('cust_data/', views.cust_data,name='cust_data')
]