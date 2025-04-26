from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.createTransaction, name='createTransaction'),
    path('<int:id>/', views.getTransaction, name='getTransaction'),
    path('update/<int:id>/', views.updateTransaction, name='updateTransaction'),
    path('delete/<int:id>/', views.deleteTransaction, name='deleteTransaction'),
    path('', views.transactionList, name='transactionList'),
]