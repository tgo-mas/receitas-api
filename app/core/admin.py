"""
Customização do Django Admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Definir as páginas de usuários para o admin"""
    ordering = ["id"]
    list_display = ["email", "name"]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissões'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_('Datas importantes'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    ]


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Receita)
admin.site.register(models.Categoria)
admin.site.register(models.Ingrediente)
