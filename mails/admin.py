from django.contrib import admin
from .models import Campaign

# Register your models here.

class CampaignAdmin(admin.ModelAdmin):
  list_display = ("name", "type", "date",)
  # prepopulated_fields = {"slug": ("name", "id")}

admin.site.register(Campaign, CampaignAdmin)