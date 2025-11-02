from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'name', 'last_name', 'sex', 'date', 'is_staff', 'is_superuser')
    list_filter = ('sex', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'name', 'last_name')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('name', 'last_name', 'email', 'sex', 'date')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'last_name', 'sex', 'date', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
