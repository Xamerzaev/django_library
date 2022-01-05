# Generated by Django 3.2.9 on 2021-11-11 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_browse', '0002_auto_20211111_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='books', to='book_browse.book'),
        ),
    ]
