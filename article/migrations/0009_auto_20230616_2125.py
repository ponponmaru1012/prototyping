# Generated by Django 3.0.3 on 2023-06-16 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_auto_20230616_2114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'Article'},
        ),
    ]
