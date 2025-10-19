from django.urls import path
from . import views

urlpatterns = [
    
    path('volunter/', views.volunter, name='volunter'),
]