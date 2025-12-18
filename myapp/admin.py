from django.contrib import admin
from .models import LoanApplication, Subscriber, Contact

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "mobile", "loan_type")
    search_fields = ("name", "mobile", "loan_type")
    list_filter = ("loan_type",)
    ordering = ("-id",)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
