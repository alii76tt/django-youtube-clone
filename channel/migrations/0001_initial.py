# Generated by Django 4.0.3 on 2022-03-27 15:50

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.CharField(max_length=120, verbose_name='Channel Name')),
                ('slogan', models.CharField(max_length=100, verbose_name='Channel Slogan')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Description')),
                ('avatar', models.ImageField(null=True, upload_to='channel/avatar/')),
                ('banner_image', models.ImageField(null=True, upload_to='channel/banner_image/')),
                ('join_date', models.DateTimeField(auto_now_add=True, verbose_name='Join Date')),
                ('subscribers', models.ManyToManyField(blank=True, related_name='video_subscribers', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
