from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from applications.accounts.models import User
# Create your models here.
class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Events(TimeStampModel):
    title = models.CharField(_('Title'), max_length=150)
    location = models.CharField(_('Location'), max_length=150)
    start_date = models.DateTimeField(_('Start Date'), max_length=150, null=False, blank=False)
    end_date = models.DateTimeField(_('End Date'), max_length=150, null=True, blank=True)
    description = models.TextField(_('Event Description'), null=True, blank=True)
    banner = models.FileField(_('Banners'), upload_to='Event-Banners', null=True, blank=True)
    user_obj = models.ForeignKey(User, null=True, blank=True, related_name='events', on_delete=models.CASCADE)
    is_published = models.BooleanField(_('Published'), default=False)
    slug = models.SlugField(_('Slug'), max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_banner_image(self):
        return self.banner.url if self.banner else settings.STATIC_URL + 'images/default_banner.jpg'

    class Meta:
        verbose_name = _('Events')
        verbose_name_plural = _('Events')
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title).lower()
        super(Events, self).save(*args, **kwargs)
