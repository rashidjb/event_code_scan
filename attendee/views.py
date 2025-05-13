from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Event, Attendee, QRCode
from .forms import RSVPForm
from django.core.files.base import ContentFile
from io import BytesIO
import qrcode
import base64


def home_view(request):
    return render(request, "attendee/home.html")


def attendee_qr_view(request, event_slug, shortcode):
    event = get_object_or_404(Event, slug=event_slug)
    qr_obj = get_object_or_404(
        QRCode, attendee__event=event, shortcode=shortcode)

    url = f"http://127.0.0.1:8000/events/{event.slug}/checkin/{qr_obj.code}/"
    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    qr_data_uri = f"data:image/png;base64,{qr_base64}"

    print(url)
    return render(request, 'qr_page.html', {
        'attendee': qr_obj.attendee,
        'event': event,
        'qr_data_uri': qr_data_uri,
        'is_used': qr_obj.is_used
    })


def check_in_view(request, event_slug, code):
    event = get_object_or_404(Event, slug=event_slug)
    qr = get_object_or_404(QRCode, code=code, attendee__event=event)
    now = timezone.now()

    # Check if QR is already used
    if qr.is_used:
        return render(request, "invalid.html", {"reason": "Already used"})

    # Check if valid time window is enforced
    if (qr.valid_from and now < qr.valid_from) or (qr.valid_until and now > qr.valid_until):
        return render(request, "invalid.html", {"reason": "Expired or not active yet"})

    # Mark as used and update attendee
    qr.is_used = True
    qr.save()
    qr.attendee.has_checked_in = True
    qr.attendee.save()

    return render(request, "success.html", {"attendee": qr.attendee})


def rsvp_view(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)

    if request.method == "POST":
        form = RSVPForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'].strip()
            last_name = form.cleaned_data['last_name'].strip()
            phone = form.cleaned_data['phone_number'].strip()

            try:
                attendee = Attendee.objects.get(
                    event=event,
                    first_name__iexact=first_name,
                    last_name__iexact=last_name,
                    phone_number__iexact=phone
                )
                qr = attendee.qrcode
                return redirect('attendee:attendee_qr', event_slug=event.slug, shortcode=qr.shortcode)
            except (Attendee.DoesNotExist, Attendee.qrcode.RelatedObjectDoesNotExist):
                return render(request, 'invitation_not_found.html', {'event': event})

    else:
        form = RSVPForm()

    return render(request, 'rsvp.html', {
        'form': form,
        'event': event
    })


class scan_qr_form_view():
    pass


class attendee_list_view():
    pass
