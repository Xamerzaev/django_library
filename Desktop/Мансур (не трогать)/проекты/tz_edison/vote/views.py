from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TimePhaseForm, FirstPhaseForm
from .models import FirstPhase, TimePhase
from django.http import HttpResponseRedirect
from django.utils import timezone
from .utils import get_win_list, reset_vote, get_data_dashboard

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'index.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginView, self).form_valid(form)

class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)

class MainView(LoginRequiredMixin, FormView):
    form_class = TimePhaseForm
    template_name = 'main.html'
    success_url = reverse_lazy('first')

    def dispatch(self, request, *args, **kwargs):
        vote = TimePhase.objects.all().last()
        now = timezone.localtime(timezone.now())

        if vote and vote.active:
            delta = vote.first * 60 - (now - vote.start).seconds
            if delta >= 0:
                return HttpResponseRedirect(reverse_lazy('first'))
            else:
                return HttpResponseRedirect(reverse_lazy('second', kwargs={'pk': vote.id}))
        return super(MainView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        phase = TimePhase.objects.all().last()
        if not phase or not phase.active:
            vote = form.save(commit=False)
            vote.user = self.request.user
            vote.save()
        return super(MainView, self).form_valid(form)

class FirstView(LoginRequiredMixin, FormView):
    form_class = FirstPhaseForm
    template_name = 'first.html'
    success_url = reverse_lazy('first')

    def get_context_data(self, **kwargs):
        context = super(FirstView, self).get_context_data(**kwargs)
        now = timezone.localtime(timezone.now())
        phase = TimePhase.objects.all().last()
        user_vote = FirstPhase.objects.filter(user=self.request.user, vote=phase)
        if user_vote:
            context['user_vote'] = True
        context['phase'] = phase
        context['delta'] = phase.first * 60 - (now - phase.start).seconds
        return context

    def form_valid(self, form):
        vote = TimePhase.objects.all().last()
        if vote.active:
            vote.votes += 1
            vote.save(update_fields=['votes'])
            first = form.save(commit=False)
            first.vote = vote
            first.user = self.request.user
            first.save()
        return super(FirstView, self).form_valid(form)

class SecondPhaseView(LoginRequiredMixin, FormView):
    form_class = FirstPhaseForm
    template_name = 'second.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('second', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(SecondPhaseView, self).get_context_data(**kwargs)
        try:
            phase = TimePhase.objects.get(id=self.kwargs['pk'])
        except TimePhase.DoesNotExist:
            return context

        if phase.votes == 0:
            reset_vote(phase)
            context['empty'] = True
            return context

        now = timezone.localtime(timezone.now())
        delta = (phase.first + phase.second) * 60 - (now - phase.start).seconds

        context['win_time'], context['win_event'], context['win_user'] = get_win_list(phase)

        if phase.active:
            if delta < 0 or not context['win_time']:
                reset_vote(phase)

        context['phase'] = phase
        context['delta'] = delta
        return context

    def form_valid(self, form):
        vote = TimePhase.objects.all().last()
        if vote.active:
            vote.votes += 1
            vote.save(update_fields=['votes'])
            first, created = FirstPhase.objects.get_or_create(vote=vote, user=self.request.user,
                                                              defaults={'time': form.cleaned_data.get('time'),
                                                                        'event': form.cleaned_data.get('event')})
            if first:
                first.time = form.cleaned_data.get('time')
                first.event = form.cleaned_data.get('event')
                first.save(update_fields=['time', 'event'])
        return super(SecondPhaseView, self).form_valid(form)


class ResetView(LoginRequiredMixin, TemplateView):
    template_name = 'reset.html'

    def get_context_data(self, **kwargs):
        context = super(ResetView, self).get_context_data(**kwargs)

        try:
            vote = TimePhase.objects.get(id=kwargs['pk'])
        except TimePhase.DoesNotExist:
            return context

        context['active'] = vote.active
        context['vote'] = kwargs['pk']

        if vote.user == self.request.user:
            context['user'] = True

            if vote.active:
                reset_vote(vote)

        return context