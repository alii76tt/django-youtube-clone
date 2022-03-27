from django.urls import path
from .views import *


app_name = "video"
urlpatterns = [
    path('', index, name="index"),
    path('watch/<slug:slug>/', videoDetail, name="detail"),
    path('create/video/', createVideo, name="createVideo"),
    path('delete/video/<int:id>/<slug:slug>/', deleteVideo, name="deleteVideo"),
    path('update/video/<int:id>/<slug:slug>/', updateVideo, name="updateVideo"),

    # sub and like
    path('watch/like/<int:id>/', likeView, name="likeVideo"),



    # like videos authorVideos
    path('like/videos', likeVideos, name="likeVideoList"),

    # author
    path('videos/', authorVideos, name="authorVideos"),

]
