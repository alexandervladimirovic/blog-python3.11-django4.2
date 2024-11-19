from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


def first_letter_upper(value):
    if value[0].islower():
        return value[0].upper() + value[1:]
    return value

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(_("Заголовок"), max_length=250, validators=[first_letter_upper])
    slug = models.SlugField("URL", max_length=250, unique_for_date='publish')
    body = models.TextField(_("Описание"))
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts', verbose_name=_("Автор"))
    created = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated = models.DateTimeField(_("Дата обновления"), auto_now=True)
    image = models.ImageField(_("Изображение"), upload_to='static/images/', blank=True, null=True)
    status = models.CharField(_("Статус"), 
                              max_length=2,
                               choices=Status.choices,
                                 default=Status.DRAFT)
    
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('main:post_detail', args=[self.publish.year,
                                                  self.publish.month,
                                                    self.publish.day,
                                                      self.slug])
    

