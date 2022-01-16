from django.contrib import admin
from .models import Events


class EventAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'user_obj', 'created', 'location', 'start_date', 'end_date', 'is_published']
    # inlines=[OpportunityWinInline,TimeStampInlie,]
    search_fields = (
        'title',
        'location'
    )
    list_filter = (
        'start_date',
        'end_date',
        'location'
    )


admin.site.register(Events, EventAdmin)
