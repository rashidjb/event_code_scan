from django.db import models
import uuid
from django.utils import timezone
import secrets
import string


def generate_shortcode(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


class Event(models.Model):
    name = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, blank=True)  # ← Add this

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Attendee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    has_checked_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.event.name})"


class QRCode(models.Model):

    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    attendee = models.OneToOneField(Attendee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_until = models.DateTimeField(null=True, blank=True)
    shortcode = models.CharField(max_length=10, blank=True)
    qr_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f"QR for {self.attendee.first_name}"

    def save(self, *args, **kwargs):
        if not self.shortcode:
            while True:
                code = generate_shortcode()
                # Enforce uniqueness manually
                if not QRCode.objects.filter(
                    attendee__event=self.attendee.event,
                    shortcode=code
                ).exists():
                    self.shortcode = code
                    break
        super().save(*args, **kwargs)
