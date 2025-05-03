from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.createTransaction, name='createTransaction'),
    path('update/<int:id>/', views.updateTransaction, name='updateTransaction'),
    path('delete/<int:id>/', views.deleteTransaction, name='deleteTransaction'),
    path('', views.transactionList, name='transactionList'),
    path('budgets/new/', views.createOrUpdateBudget, name='createOrUpdateBudget'),
    path('budgets/', views.getBudget, name='getBudget'),
    path('budgets/all/', views.budgetList, name='budget-list'),
    path('<int:id>/', views.getTransaction, name='getTransaction'),
]