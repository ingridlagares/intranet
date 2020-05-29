from django.contrib import admin
from .models import Area, Pessoa
# Register your models here.

class AreaAdmin(admin.ModelAdmin):

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('nome',)
    list_filter = ('nome',)
    fieldsets = (
        (None, {'fields': ('nome',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('nome',)
            }
        ),
    )

    ordering = ('nome',)
    filter_horizontal = ()


admin.site.register(Area, AreaAdmin)
admin.site.register(Pessoa)
