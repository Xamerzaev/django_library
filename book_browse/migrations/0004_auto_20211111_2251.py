# Generated by Django 3.2.9 on 2021-11-11 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_browse', '0003_alter_author_book'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='book',
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='book_browse.author'),
        ),
    ]
