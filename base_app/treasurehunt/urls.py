from django.urls import path
from . import views
app_name = 'treasurehunt'

urlpatterns = [
    path('register/', views.register, name='register'),
]
