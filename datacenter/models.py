from django.db import models
from django.utils.timezone import localtime
import django


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f"{self.owner_name} (inactive)"


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f"leaved at {self.leaved_at}"
                if self.leaved_at
                else "not leaved"
            ),
        )


def get_duration(visit):
    now = django.utils.timezone.localtime()
    try:
        duration = localtime(visit.leaved_at) - localtime(visit.entered_at)
    except TypeError:
        duration = now - localtime(visit.entered_at)
    return duration


def format_duration(duration):
    minutes_in_hour = 60
    seconds_in_minute = 60
    seconds_in_hour = minutes_in_hour * seconds_in_minute
    duration_in_seconds = duration.total_seconds()
    hours = int(duration_in_seconds // seconds_in_hour)
    minutes = int(
        (duration_in_seconds - hours * seconds_in_hour) // seconds_in_minute
    )
    return f"{hours}ч {minutes}мин"


def is_visit_long(visit, minutes=60):
    seconds_in_minute = 60
    duration = get_duration(visit)
    return int(duration.total_seconds()) < minutes * seconds_in_minute
