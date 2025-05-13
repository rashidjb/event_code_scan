from django.urls import path
from . import views

app_name = "attendee"

urlpatterns = [
    path('<slug:event_slug>/rsvp/', views.rsvp_view, name='rsvp'),
    path('<slug:event_slug>/<str:shortcode>/',
         views.attendee_qr_view, name='attendee_qr'),
    path('<slug:event_slug>/scan/', views.scan_qr_form_view, name='scan_qr'),
    path('<slug:event_slug>/checkin/<uuid:code>/',
         views.check_in_view, name='check_in'),
    path('<slug:event_slug>/list/', views.attendee_list_view, name='attendee_list'),
]
