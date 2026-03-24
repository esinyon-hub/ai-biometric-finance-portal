from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_register, name='biometric_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('bypass-login/', views.bypass_login, name='bypass_login'),  # <-- bypass button
    path('add-budget/', views.add_budget, name='add_budget'),
    path('add-expense/', views.add_expense, name='add_expense'),
]