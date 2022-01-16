from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _


# Create your models here.
class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class User(AbstractUser, TimeStampModel):
    image = models.ImageField(upload_to='profiles', null=True, blank=True)

    def get_image(self):
        return self.image.url if self.image else settings.STATIC_URL + 'images/profile.jpg'

    # def get_thumbnail(self):
    #     try:
    #         return get_thumbnail(self.image, '50x50', crop='center', quality=99).url
    #     except:
    #         return self.get_image()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('Users')
        verbose_name_plural = _('Users')
        ordering = ('-created',)
