from django.urls import path
from . import views

app_name = "adminpanel"

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("users/", views.users_list, name="users_list"),
    path("users/<int:user_id>/", views.user_detail, name="user_detail"),
    path("users/<int:user_id>/verify/", views.verify_user, name="verify_user"),

    path("helps/", views.helps_list, name="helps_list"),
    path("helps/<int:help_id>/", views.help_detail, name="help_detail"),
    path("helps/<int:help_id>/approve/", views.approve_help, name="approve_help"),
    path("helps/<int:help_id>/reject/", views.reject_help, name="reject_help"),

    path("profile/", views.admin_profile, name="admin_profile"),
    path("profile/edit/", views.admin_edit_profile, name="admin_edit_profile"),

    path('helps/resubmit/<int:help_id>/', views.request_resubmit_help, name='request_resubmit_help'),


]
