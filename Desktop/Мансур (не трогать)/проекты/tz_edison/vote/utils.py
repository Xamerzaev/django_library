import json 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from collections import Counter

from .models import FirstPhase


def get_win_list(phase):
    lst, win_time, win_event, win_user = [], [], [], []
    first = FirstPhase.objects.filter(vote=phase.id)

    for fir in first:
        if fir.time < 10:
            time = "0" + str(fir.time)
        else:
            time = str(fir.time)
        lst.append(time + str(fir.event))

    count = Counter(lst)
    max_value = max(count.values())
    max_keys = [k for k, v in count.items() if v == max_value]

    if len(max_keys) == 1:
        win_time = max_keys[0][:2]
        if win_time[0] == '0':
            win_time = win_time[1]
        win_event = max_keys[0][2:]
        users = FirstPhase.objects.filter(vote=phase.id, time=win_time,
                                          event=win_event).values_list('user__username', flat=True)
        for win in users:
            win_user.append(win)

    return win_time, win_event, win_user


# Сброс голосования
def reset_vote(phase):
    phase.active = False
    phase.save(update_fields=['active'])
    return

@login_required()
def get_data_dashboard(request):
    phases = request.GET.get('phase')
    time = {}
    for i in range(0, 24):
        event = {'len': 0}
        phase = FirstPhase.objects.filter(vote=phases, time=i)
        phase_event = phase.values_list('event', flat=True)
        if phase_event:
            for x in phase_event:
                u = phase.filter(event=x)
                us = []
                event['len'] += 1
                users = list(u.values_list('user', flat=True))
                for user in users:
                    us.append(User.objects.get(id=user).username)
                event[x] = us
            time[str(i)] = event
        else:
            time[str(i)] = ['']
    return JsonResponse(time)

@login_required()
def get_event(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        events = FirstPhase.objects.filter(event__istartswith=q)
        results = []
        for ev in events:
            if ev.event not in results:
                results.append(ev.event)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)