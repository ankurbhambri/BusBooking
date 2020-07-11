from django.contrib import admin
from accounts.models import CustomerLogin


@admin.register(CustomerLogin)
class CustomerLoginAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone_number", "customer_email",
                    "created_date", "modified_date")
    search_fields = ("id", "name", "customer_email", "phone_number")
