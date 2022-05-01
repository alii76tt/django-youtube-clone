from django.contrib import admin
from .models import *


class VideoAdmin(admin.ModelAdmin):

    list_display = ['title', 'publishing_date', 'image_tag', ]
    list_filter = ['publishing_date']
    search_fields = ['title']

    class Meta:
        model = Video


admin.site.register(Video, VideoAdmin)
admin.site.register(Comment)
admin.site.register(WatchLater)
