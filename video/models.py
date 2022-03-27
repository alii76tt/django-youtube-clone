from statistics import mode
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from channel.models import Channel


class Video(models.Model):
    STATUS = [
        ('True', 'True'),
        ('False', 'False'),
    ]
    user = models.ForeignKey('auth.User', verbose_name='Author',
                             related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=120, verbose_name="Video Title")
    content = RichTextField(verbose_name="Video Description")
    cover_image = models.ImageField(null=True, upload_to='video/cover_image/')
    video = models.FileField(upload_to='videos/')
    status = models.CharField(default="True",choices=STATUS,max_length=6)
    slug = models.SlugField(unique=True, editable=False, max_length=200)
    publishing_date = models.DateTimeField(
        verbose_name="Publishing Date", auto_now_add=True)
    likes = models.ManyToManyField(
        User, related_name="video_posts", blank=True)
    channel = models.ForeignKey(
        Channel, related_name='channel', null=True, on_delete=models.CASCADE)

    def image_tag(self):
        if self.cover_image:
            return mark_safe(f'<img src="{self.cover_image.url}" height="100"/>')

    image_tag.short_description = "Image"
    image_tag.allow_tags = True

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("video:detail", kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('video:updateVideo', kwargs={'slug': self.slug, 'id': self.id})

    def get_delete_url(self):
        return reverse('video:deleteVideo', kwargs={'slug': self.slug, 'id': self.id})

    def get_unique_slug(self):
        slug = slugify(self.title.replace('ı', 'i'))
        unique_slug = slug
        counter = 1
        while Video.objects.filter(slug=unique_slug):
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        self.slug = self.get_unique_slug()
        return super(Video, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-publishing_date', 'id']


class Comment(models.Model):
    video = models.ForeignKey(
        Video, related_name='comments', null=True, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, verbose_name='Channel',
                                related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField(max_length=300)
    date_added = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    def __str__(self):
        return str(self.channel.channel_name)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-date_added').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
