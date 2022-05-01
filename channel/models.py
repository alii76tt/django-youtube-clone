from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.safestring import mark_safe


class Channel(models.Model):
    channel_name = models.CharField(
        max_length=120, verbose_name="Channel Name")
    slogan = models.CharField(max_length=100, verbose_name="Channel Slogan")
    subscribers = models.ManyToManyField(
        User, related_name="video_subscribers", blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = RichTextField(verbose_name="Description", blank=True)
    avatar = models.ImageField(upload_to='channel/avatar/', default="images/channel/avatar/avatar.png")
    banner_image = models.ImageField(upload_to='channel/banner_image/', default="images/channel/avatar/avatar.png")
    join_date = models.DateTimeField(
        verbose_name="Join Date", auto_now_add=True)
    
    def image_tag(self):
        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url}" height="100">')

    image_tag.short_description = "Image"
    image_tag.allow_tags = True

    def __str__(self):
        return self.channel_name

    def get_absolute_url(self):
        return reverse("channel:channelDetail", kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('channel:updateChannel', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('channel:deleteChannel', kwargs={'id': self.id})

    def total_subscribers(self):
        return self.subscribers.count()