from django.contrib import admin
from .models import Channel


class ChannelAdmin(admin.ModelAdmin):

    list_display = ['channel_name', 'join_date', 'image_tag', ]
    list_filter = ['join_date']
    search_fields = ['channel_name']

    class Meta:
        model = Channel


# Register your models here.
admin.site.register(Channel, ChannelAdmin)
