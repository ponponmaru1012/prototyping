# Generated by Django 3.0.3 on 2022-07-15 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20220706_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bg_image',
            field=models.ImageField(blank=True, null=True, upload_to='bgimage/', verbose_name='Backgroung Image'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='fb_link',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook Link'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icon/', verbose_name='Icon Image'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='ig_link',
            field=models.URLField(blank=True, null=True, verbose_name='Instagram Link'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='introduction',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Introduction'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profession',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Profession'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='tw_link',
            field=models.URLField(blank=True, null=True, verbose_name='Twitter Link'),
        ),
    ]
