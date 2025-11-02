from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    path('volunteer/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('help/', views.create_help_request, name='help'),
    path('help/edit/<int:pk>/', views.edit_request, name='edit_request'),
    path('help/delete/<int:pk>/', views.delete_request, name='delete_request'),
    path('help/detail/<int:pk>/', views.request_detail, name='request_detail'),
    path('help/accept/<int:pk>/', views.accept_request, name='accept_request'),
    path('help/reject/<int:pk>/', views.reject_request, name='reject_request'),
]
