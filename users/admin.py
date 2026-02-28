from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 🔹 Campos visibles en la lista del admin
    list_display = ('email', 'name', 'last_name', 'is_staff', 'is_verified')
    ordering = ('email',)
    search_fields = ('email', 'name', 'last_name')

    # 🔹 Agrupación de campos en el formulario de edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('name', 'last_name', 'sex', 'date', 'phone_number', 'dni', 'profile_image')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    # 🔹 Campos visibles cuando se crea un nuevo usuario desde el admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'last_name', 'sex', 'date',
                'phone_number', 'dni', 'profile_image',
                'password1', 'password2', 'is_staff', 'is_verified'
            ),
        }),
    )

    # 🔹 Campos solo lectura opcionales
    readonly_fields = ('last_login', 'date_joined')

    # 🔹 Para evitar errores al eliminar username
    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields.pop('username', None)  # <- 🔥 asegura que no intente mostrar username
        return form
