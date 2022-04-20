from django.contrib import admin
from .models import Amount, Area


class AmountAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount']
    search_fields = ['amount']


class AreaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


admin.site.register(Amount, AmountAdmin)
admin.site.register(Area, AreaAdmin)
