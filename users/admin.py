from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'title']
    fieldsets = (
        (
            None, {
                'fields': ('email', 'title')
            }
        ),
        (
            'Personal info', {
                'fields': (
                    'first_name', 'last_name',
                    'phone', 'profile', 'password'
                )
            }
        ),
        (
            'Permissions', {
                'fields': ('is_admin', 'is_active')
            }
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
