from django.contrib import admin
from .models import Projeto, Area, ProjetoIntegrante, ProjetoArea


# Register your models here.
class ProjetoAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('titulo', 'coordenador')
    list_filter = ('coordenador',)
    fieldsets = (
        (
            None, {
                'fields': ('titulo', 'sigla', 'coordenador',)
            }
        ),
        (
            'Duração', {
                'fields': ('inicio', 'termino')
            }
        ),
        (
            'Informações', {
                'fields': (
                    'descricao', 'agencia', 'programa',
                    'natureza', 'situacao', 'processo',
                    'resolucao', 'imagem_divulgacao'
                )
            }
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('titulo',)
            }
        ),
    )
    ordering = ('titulo',)
    filter_horizontal = ()


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


class ProjetoAreaAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('projeto', 'area')
    list_filter = ('area',)
    fieldsets = (
            (None, {'fields': ('projeto', 'area',)}),
    )


class ProjetoIntegranteAdmin(admin.ModelAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('integrante', 'projeto')
    list_filter = ('projeto',)
    fieldsets = (
        (None, {'fields': ('projeto', 'integrante',)}),
    )


admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(ProjetoIntegrante, ProjetoIntegranteAdmin)
admin.site.register(ProjetoArea, ProjetoAreaAdmin)
