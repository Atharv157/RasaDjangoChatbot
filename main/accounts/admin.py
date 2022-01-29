from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','dob','gender','pan','phoneno'
    )
    search_fields = ('email','pan')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Customer,AccountAdmin)


admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(Account)
admin.site.register(Complaint)
admin.site.register(Card)
admin.site.register(Branch)
