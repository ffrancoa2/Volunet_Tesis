from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/',views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.edit_profile, name='profile'),
    path('update-profile-image/', views.update_profile_image, name='update_profile_image'),
    path("verify/", views.verify_account, name="verify_account")

]