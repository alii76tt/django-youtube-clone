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

    # library
    path('library/', userLibrary, name="userLibrary"),
    path('library/<int:id>/', userLibraryVideos, name="userLibraryVideos"),
    path('create/library/', userLibraryCreate, name="userLibraryCreate"),
    path('update/library/<int:id>/', userLibraryUpdate, name="userLibraryUpdate"),
    path('delete/library/<int:id>/', userLibraryDelete, name="userLibraryDelete"),

    path('add/library/video/<int:id>/<int:video_id>/', addLibraryVideo, name="addLibraryVideo"),
    path('remove/library/video/<int:id>/<int:video_id>/', removeLibraryVideo, name="removeLibraryVideo"),


    # like videos authorVideos
    path('like/videos', likeVideos, name="likeVideoList"),

    # author
    path('author/videos/', authorVideos, name="authorVideos"),

]
