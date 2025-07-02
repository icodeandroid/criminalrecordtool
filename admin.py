from django.contrib import admin
from .models import CriminalRecord

@admin.register(CriminalRecord)
class CriminalRecordAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = [
        'defendant_name', 
        'case_number', 
        'date_filed', 
        'parish', 
        'sex', 
        'race', 
        'alert_available',
        'scraped_timestamp'
    ]
    
    # Fields that can be clicked to view the record
    list_display_links = ['defendant_name', 'case_number']
    
    # Filters in the right sidebar
    list_filter = [
        'sex',
        'race', 
        'parish',
        'alert_available',
        'date_filed',
        'scraped_timestamp',
    ]
    
    # Search functionality
    search_fields = [
        'defendant_name',
        'case_number',
        'charges',
        'parish'
    ]
    
    # Fields to show when editing/adding records
    fieldsets = (
        ('Defendant Information', {
            'fields': ('defendant_name', 'birth_date', 'sex', 'race')
        }),
        ('Case Information', {
            'fields': ('case_number', 'date_filed', 'arrest_citation_date', 'parish')
        }),
        ('Charges', {
            'fields': ('charges',),
            'description': 'Enter multiple charges separated by semicolons or on separate lines'
        }),
        ('System Information', {
            'fields': ('alert_available', 'scraped_timestamp'),
            'classes': ('collapse',)  # This section will be collapsible
        }),
    )
    
    # Make case_number readonly after creation to prevent accidental changes
    readonly_fields = ['created_at', 'updated_at']
    
    # Default ordering
    ordering = ['-scraped_timestamp']
    
    # Number of records per page
    list_per_page = 25
    
    # Enable date hierarchy navigation
    date_hierarchy = 'date_filed'
    
    # Actions
    actions = ['mark_alert_available', 'mark_alert_unavailable']
    
    def mark_alert_available(self, request, queryset):
        queryset.update(alert_available=True)
        self.message_user(request, f"{queryset.count()} records marked as alert available.")
    mark_alert_available.short_description = "Mark selected records as alert available"
    
    def mark_alert_unavailable(self, request, queryset):
        queryset.update(alert_available=False)
        self.message_user(request, f"{queryset.count()} records marked as alert unavailable.")
    mark_alert_unavailable.short_description = "Mark selected records as alert unavailable"