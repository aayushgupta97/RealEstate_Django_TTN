from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<int:user_id>', views.update_user, name="update_user_details")
]
