from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from video.forms import CommentForm, VideoForm
from .models import *
from channel.models import Channel
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def likeView(request, id):
    if Channel.objects.filter(user_id=request.user.id).exists():
        video = get_object_or_404(Video, id=request.POST.get('video_id'))
        liked = False
        if video.likes.filter(id=request.user.id).exists():
            video.likes.remove(request.user)
            liked = False
        else:
            video.likes.add(request.user)
            liked = True

        url = request.META.get('HTTP_REFERER')
    else:
        messages.warning(request, 'You must create a channel to like videos!')
        return redirect('channel:createChannel')

    return HttpResponseRedirect(url)



# video


def index(request):

    video_list = Video.objects.filter(status="True")

    paginator = Paginator(video_list, 15)  # Show 15 contacts per page

    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        videos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        videos = paginator.page(paginator.num_pages)

    query = request.GET.get('q')
    if query:
        videos = video_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)).distinct()

    context = {
        'videos': videos,
    }
    return render(request, 'video/index.html', context)


def videoDetail(request, slug):
    video = get_object_or_404(Video, slug=slug)
    channel = Channel.objects.get(channel=video.id)
    comments = Comment.objects.filter(video=video, parent=None)
    try:
        channel_id = Channel.objects.get(user_id=request.user.id)
    except:
        channel_id = 1

    liked = False
    if video.likes.filter(id=request.user.id).exists():
        liked = True

    subscribe = False
    if channel.subscribers.filter(id=request.user.id).exists():
        subscribe = True

    url = request.META.get('HTTP_REFERER')
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            if Channel.objects.filter(user_id=request.user.id).exists():
                form.instance.video = video
                form.instance.channel_id = channel_id.id
                parent_id = request.POST.get('comment_id')
                comment_qs = None
                if parent_id:
                    comment_qs = Comment.objects.get(id=parent_id)
                form.instance.parent = comment_qs
                form.save()
                messages.success(request, 'Your comment has been added.')
            else:
                messages.warning(
                request, 'You must create a channel to subscribe channels!')
                return redirect('channel:createChannel')

            return HttpResponseRedirect(url)
        else:
            messages.warning(request, 'Your comment could not be added!')

    context = {
        'videos': Video.objects.filter(status="True")[:5],
        'video': video,
        'comments': comments,
        'channel': channel,
        'form': form,
        'liked': liked,
        'likes_total': video.total_likes(),
        'subscribe': subscribe,
        'subscribe_total': channel.total_subscribers()
    }
    return render(request, 'video/detail.html', context)

@login_required
def createVideo(request):
    if Channel.objects.filter(user_id=request.user.id):
        channel_id = Channel.objects.get(user_id=request.user.id)
        videoForm = VideoForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if videoForm.is_valid():
                videoForm.instance.user_id = request.user.id
                videoForm.instance.channel_id = channel_id.id
                video = videoForm.save()
                messages.success(
                    request, 'Your video has been successfully created.')
                return HttpResponseRedirect(video.get_absolute_url())
            else:
                messages.warning(request, 'Your video could not be created!')
    else:
        messages.warning(
            request, 'You must create a channel to upload videos!')
        return redirect('channel:createChannel')

    return render(request, 'video/post/create_video.html', {'videoForm': videoForm})


@login_required
def updateVideo(request, id, slug):
    if Channel.objects.filter(user_id=request.user.id):
        video = Video.objects.get(id=id, slug=slug, user_id=request.user.id)
        channel_id = Channel.objects.get(user_id=request.user.id)

        videoForm = VideoForm(request.POST or None,
                            request.FILES or None, instance=video)
        if request.method == "POST":
            if videoForm.is_valid():
                videoForm.instance.user_id = request.user.id
                videoForm.instance.channel_id = channel_id.id
                videoForm.save()
                messages.success(
                    request, 'Your video has been successfully updated.')
                return HttpResponseRedirect(video.get_absolute_url())
            else:
                messages.warning(request, 'Your video could not be updated!')
    else:
        messages.warning(
        request, 'You must create a channel to upload videos!')
        return redirect('channel:createChannel')

    return render(request, 'video/post/update_video.html', {'videoForm': videoForm})


@login_required
def deleteVideo(request, id, slug):
    if Channel.objects.filter(user_id=request.user.id):
        video = Video.objects.get(id=id, slug=slug, user_id=request.user.id)
        try:
            video.delete()
            messages.success(request, "Your video has been successfully deleted.")
        except:
            messages.error(request, "Your video could not be deleted!")
    else:
        messages.warning(
        request, 'You must create a channel to upload videos!')
        return redirect('channel:createChannel')

    return redirect('video:index')

# like videos


def likeVideos(request):
    context = {
        'videos': Video.objects.filter(status="True", likes=request.user.id),
    }
    return render(request, 'video/like_videos_list.html', context)

# author videos


def authorVideos(request):
    context = {
        'videos': Video.objects.filter(status="True", user_id=request.user.id),
    }
    return render(request, 'video/author_videos.html', context)
