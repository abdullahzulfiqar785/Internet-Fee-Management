from django.contrib import admin
from .models import Customer, Fee


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'cnic', 'phone', 'area', 'fee']
    search_fields = ['name', 'cnic', 'phone', 'area', ]
    autocomplete_fields = ['fee', 'area']


class FeeAdmin(admin.ModelAdmin):
    list_display = ['customer', 'recipient', 'amount_paid']
    autocomplete_fields = ['customer', 'recipient']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Fee, FeeAdmin)
