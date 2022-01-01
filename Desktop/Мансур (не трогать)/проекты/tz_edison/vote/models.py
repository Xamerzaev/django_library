from django.db import models

from django.contrib.auth.models import User


class TimePhase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first = models.IntegerField(verbose_name='Длительность первой фазы')
    second = models.IntegerField(verbose_name='Длительность второй фазы')
    active = models.BooleanField(default=True, verbose_name='Голосование активно')
    votes = models.IntegerField(default=0, verbose_name='Всего проголосовало')
    start = models.DateTimeField(auto_now=True, verbose_name="Начало голосования")

    def __str__(self):
        return str(self.id)

class FirstPhase(models.Model):
    vote = models.ForeignKey(TimePhase,on_delete=models.CASCADE,verbose_name="Номер голосования")
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Пользователь')
    time = models.IntegerField(verbose_name='Время')
    event = models.CharField(max_length=255, verbose_name='Мероприятие')
    start = models.DateTimeField(auto_now=True, verbose_name="Начало голосования")