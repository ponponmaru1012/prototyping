from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    username = models.CharField(
        _("username"),
        max_length=30,
        help_text='Required 30 characters or fewer.',
        unique=True,
        error_messages={
            'unique': _("This Username already exists."),
        },)

    email = models.EmailField(
        _('email'),
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        },)

    fb_link = models.URLField(verbose_name='Facebook Link', null=True, blank=True)

    ig_link = models.URLField(verbose_name='Instagram Link', null=True, blank=True)

    tw_link = models.URLField(verbose_name='Twitter Link', null=True, blank=True)

    bg_image = models.ImageField(verbose_name='Backgroung Image', null=True, blank=True, upload_to='bgimage/')

    icon = models.ImageField(verbose_name='Icon Image', null=True, blank=True, upload_to='icon/')

    profession = models.CharField(verbose_name='Profession', null=True, blank=True, max_length=20)

    introduction = models.TextField(verbose_name='Introduction', null=True, blank=True, max_length=500)
    
    class Meta:
        verbose_name_plural = 'CustomUser'


