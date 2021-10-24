from django.db import models

# Create your models here.
class User(models.Model):
    name = models.TextField()
    surname = models.TextField()
    def __str__(self) -> str:
        return self.name[:15]
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'