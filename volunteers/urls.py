from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    path('volunteer/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('help/', views.create_help_request, name='help'),
    path('help/edit/<int:pk>/', views.edit_request, name='edit_request'),
    path('help/delete/<int:pk>/', views.delete_request, name='delete_request'),
    path('help/detail/<int:pk>/', views.request_detail, name='request_detail'),
    path('help/reject/<int:pk>/', views.reject_request, name='reject_request'),

    # Mis actividades
    path('my-requests/', views.my_requests, name='my_requests'),
    path('my-donations/', views.my_donations, name='my_donations'),

    # Donación
    path('donate/<int:pk>/', views.donate_to_help, name='donate_to_help'),
    path('donation/success/<int:pk>/', views.donation_success, name='donation_success'),
]
