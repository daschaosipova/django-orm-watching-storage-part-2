from datacenter.models import Visit
from datacenter.models import get_duration
from datacenter.models import format_duration
from datacenter.models import is_visit_long
from django.shortcuts import render
from django.utils.timezone import localtime


def storage_information_view(request):
    not_leaved = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []
    for visit in not_leaved:
        duration = get_duration(visit)
        visit_data = {
            'who_entered': visit.passcard,
            'entered_at': localtime(visit.entered_at),
            'duration': format_duration(duration),
            'is_strange': is_visit_long(visit, 60),
        }
        non_closed_visits.append(visit_data)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
