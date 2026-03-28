from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import is_visit_long
from datacenter.models import get_duration
from datacenter.models import format_duration
from django.shortcuts import render
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    passcards_visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in passcards_visits:
        duration = get_duration(visit)
        visit_info = {
            'entered_at': localtime(visit.entered_at),
            'duration': format_duration(duration),
            'is_strange': is_visit_long(visit, 60)
        }
        this_passcard_visits.append(visit_info)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
