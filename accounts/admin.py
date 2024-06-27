from django.contrib import admin
from .models import CustomUser, Contact, Status, CustomToken, Opportunity, OTPToken

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'personal_email', 'phone_number', 'report_to', 'city', 'region', 'country')
    list_filter = ('city', 'region', 'country')
    


admin.site.register(OTPToken)


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ['opportunity_name', 'account_name', 'amount', 'rating', 'close_date']
    list_editable = ["close_date", "amount"]
    search_fields = ['opportubity_name', 'account_name']


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['opportunity', 'stage', 'next_step']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "is_active"]
    list_editable = ["is_active"]
    search_fields = ["username", "email"]




@admin.register(CustomToken)
class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ["get_owner_username", "access_token_expires_at", "refresh_token_expires_at"]
    list_filter = ["user"]
    search_fields = ["user"]

    def get_owner_username(self, obj):
        return obj.user.username
    get_owner_username.short_description = 'Username'

    
