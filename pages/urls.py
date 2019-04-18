from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('error_404', views.handler404, name="error404"),
    # path('error_500', views.handler500, name="error500"),

]
