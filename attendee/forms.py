# attendee/forms.py
from django import forms
from django.core.validators import RegexValidator


class RSVPForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(
        max_length=8,
        min_length=8,
        validators=[
            RegexValidator(
                r'^\d{8}$', message="Enter an 8-digit Kuwaiti phone number")
        ]
    )
