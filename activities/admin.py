from django.contrib import admin
from .models import Activity

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_activitytype_display', 'get_shift_display', 'status')

admin.site.register(Activity, ActivityAdmin)
