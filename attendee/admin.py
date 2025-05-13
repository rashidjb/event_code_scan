from django.contrib import admin
from .models import Event, Attendee, QRCode


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_datetime', 'end_datetime', 'location')


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',
                    'phone_number', 'event', 'has_checked_in')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('event', 'has_checked_in')


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'attendee', 'is_used',
                    'valid_from', 'valid_until', 'created_at')
    list_filter = ('is_used',)
