from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *
# Register your models here.


class CustomerAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','dob','gender','pan','phoneno'
    )
    search_fields = ('email','pan')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Customer,CustomerAdmin)

class BranchAdmin(admin.ModelAdmin):
    list_display = ('ifsc','contact','location'
    )
    search_fields = ('ifsc','location')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Branch, BranchAdmin)

class AccountAdmin(admin.ModelAdmin):
    list_display = ('acc_no', 'balance','acc_type', 'is_blocked', 'customer_id', 'branch_id', 'open_date'
    )
    search_fields = ('acc_no','is_blocked', 'open_date', 'customer_id', 'acc_type')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account, AccountAdmin)

class CardAdmin(admin.ModelAdmin):
    list_display = ('is_blocked', 'card_no','acc_no', 'card_type', 'pin', 'credit_used', 'exp_date'
    )
    search_fields = ('is_blocked','card_no','acc_no', 'exp_date')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Card, CardAdmin)

admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(Complaint)
