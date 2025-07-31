from django.urls import path
from . import views

app_name = 'financial'

urlpatterns = [
    path('', views.financial_dashboard, name='dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.create_transaction, name='create_transaction'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/create/', views.create_budget, name='create_budget'),
    path('bank-accounts/', views.bank_accounts, name='bank_accounts'),
    path('bank-accounts/create/', views.create_bank_account, name='create_bank_account'),
]