from django.contrib import admin
from .models import SubscriptionPlan, PricingTier, Subscription


class PricingTierInline(admin.TabularInline):
    model = PricingTier
    extra = 1


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'plan_type', 'status']
    list_filter = ['plan_type', 'status', 'branch']
    inlines = [PricingTierInline]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'plan', 'start_date']
    list_filter = ['start_date']
    search_fields = ['studentlast_name', 'subjectname']