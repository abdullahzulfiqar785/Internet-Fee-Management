from django.contrib import admin
from django.http import HttpResponse
from .models import Customer, Fee
from .utils import get_id, get_date, render_to_pdf
import datetime


class FeeAdminInline(admin.ModelAdmin):
    # model = Fee
    # extra = 0
    search_fields = ['customer__customer_id', ]
    list_display = ['customer', 'pay_date',
                    'recipient', 'amount_paid', 'credit']
    autocomplete_fields = ['customer', 'recipient']
    readonly_fields = ['recipient', 'credit', 'pay_date', ]
    date_hierarchy = 'pay_date'

    def save_model(self, request, obj, form, change) -> None:
        paying = obj.amount_paid
        cus_fee = obj.customer.fee.amount
        obj.pay_date = get_date(obj)
        current_month = obj.pay_date.month
        current_year = obj.pay_date.year

        if Fee.objects.filter(customer=obj.customer, credit__gt=0).exists():
            credit_wala_object = Fee.objects.filter(
                customer=obj.customer, credit__gt=0).first()
            if paying > credit_wala_object.credit:
                paying = paying - credit_wala_object.credit
                credit_wala_object.credit = 0
                credit_wala_object.amount_paid = cus_fee
                credit_wala_object.save()
                if paying == cus_fee:
                    obj.amount_paid = paying
            elif paying <= credit_wala_object.credit:
                obj.amount_paid = 0
                left_credit = 0 if paying == credit_wala_object.credit else credit_wala_object.credit - paying
                credit_wala_object.credit = 0
                left_fee = cus_fee - credit_wala_object.amount_paid
                credit_wala_object.amount_paid = cus_fee
                credit_wala_object.save()
                obj.credit = cus_fee + left_credit + left_fee
                paying = 0
                obj.recipient = request.user
                obj.save()
                pdf = render_to_pdf("invoice/invoice.html")
                print(type(pdf))
                return super().save_model(request, obj, form, change)

        if paying > cus_fee:
            obj.amount_paid = cus_fee
            paying = paying - cus_fee

            while paying > 0:
                current_month = current_month+1
                if current_month > 12:
                    current_year = current_year + 1
                    current_month = 1
                date = datetime.date(
                    current_year, current_month, obj.pay_date.day)
                fee = Fee(customer=obj.customer, recipient=request.user,
                          amount_paid=cus_fee if paying > cus_fee else paying, pay_date=date)
                paying = paying - cus_fee
                fee.save()
            customerFee = Fee.objects.filter(
                customer=obj.customer).latest('id')
            if not customerFee.amount_paid == cus_fee:
                customerFee.credit = cus_fee - customerFee.amount_paid
                customerFee.save()
        elif paying < cus_fee:
            obj.amount_paid = paying
            obj.credit = obj.credit + (cus_fee - paying)

        obj.recipient = request.user
        return super().save_model(request, obj, form, change)


class CustomerAdmin(admin.ModelAdmin):
    # inlines = [FeeAdminInline, ]
    list_display = ['name', 'customer_id', 'phone', 'area', 'fee', ]
    search_fields = ['name', 'customer_id']
    autocomplete_fields = ['fee', 'area']
    readonly_fields = ['customer_id']

    def save_model(self, request, obj, form, change) -> None:
        obj.customer_id = get_id()
        return super().save_model(request, obj, form, change)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Fee, FeeAdminInline)
