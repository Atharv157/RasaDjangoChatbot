from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Customer
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','dob','gender','pan'
    )
    search_fields = ('email','pan')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(Customer,AccountAdmin)