from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Activity

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("who", "day", "title", "start_time", "end_time", "location")
    list_filter = ("who", "day")
    search_fields = ("who", "title", "location", "notes")
