from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from .models import Channel
from .forms import ChannelForm
from video.models import Video
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def subscribeView(request, id):
    if Channel.objects.filter(user_id=request.user.id).exists():
        channel = get_object_or_404(
            Channel, id=request.POST.get('video_subscribe_id'))
        subscribe = False
        if channel.subscribers.filter(id=request.user.id).exists():
            channel.subscribers.remove(request.user)
            subscribe = False
        else:
            channel.subscribers.add(request.user)
            subscribe = True

        url = request.META.get('HTTP_REFERER')
    else:
        messages.warning(
            request, 'You must create a channel to subscribe channels!')
        return redirect('channel:createChannel')

    return HttpResponseRedirect(url)


def channelList(request):
    channels = Channel.objects.all()[:10]
    context = {
        'channels': channels,
    }
    return render(request, 'channel/channel_list.html', context)


def channelDetail(request, id):
    channel = Channel.objects.get(id=id)
    videos = Video.objects.filter(status="True", channel_id=id)

    subscribe = False
    if channel.subscribers.filter(id=request.user.id).exists():
        subscribe = True

    context = {
        'channel': channel,
        'videos': videos,
        'last_video': videos.last(),
        'subscribe': subscribe,
        'subscribe_total': channel.total_subscribers(),
    }


    return render(request, 'channel/channel_detail.html', context)


@login_required
def createChannel(request):
    if not Channel.objects.filter(user_id=request.user.id).exists():
        channelForm = ChannelForm(request.POST or None, request.FILES or None)
        if request.method == "POST":
            if channelForm.is_valid():
                channelForm.instance.user_id = request.user.id
                channel = channelForm.save()
                messages.success(
                    request, 'Your channel has been successfully created.')
                return HttpResponseRedirect(channel.get_absolute_url())
    else:
        userChannel = Channel.objects.get(user_id=request.user.id)
        messages.warning(request, 'You already own a channel!')
        return HttpResponseRedirect(userChannel.get_absolute_url())

    return render(request, 'channel/post/create_channel.html', {'channelForm': channelForm})


@login_required
def updateChannel(request, id):
    if Channel.objects.filter(user_id=request.user.id).exists():
        channel = Channel.objects.get(id=id, user_id=request.user.id)
        channelForm = ChannelForm(
            request.POST or None, request.FILES or None, instance=channel)
        if request.method == "POST":
            if channelForm.is_valid():
                channelForm.instance.user_id = request.user.id
                channelForm.save()
                messages.success(
                    request, 'Your channel has been successfully created.')
                return HttpResponseRedirect(channel.get_absolute_url())
    else:
        messages.warning(request, 'Please create your channel!')
        return redirect('video:createChannel')

    return render(request, 'channel/post/update_channel.html', {'channelForm': channelForm})


@login_required
def deleteChannel(request, id):
    if Channel.objects.filter(user_id=request.user.id).exists():
        channel = Channel.objects.get(id=id, user_id=request.user.id)
        try:
            channel.delete()
            messages.success(
                request, "Your channel has been successfully deleted.")
        except:
            messages.error(request, "Your channel could not be deleted!")
    else:
        messages.warning(request, 'Please create your channel!')
        return redirect('video:createChannel')

    return redirect('video:index')

def subscriptionsList(request):
    videos = Video.objects.raw(f"SELECT * from video_video WHERE channel_id=(SELECT channel_id FROM channel_channel_subscribers WHERE user_id={request.user.id})")
    context = {
        'channels': Channel.objects.filter(subscribers=request.user.id),
        'videos': videos
    }
    return render(request, 'channel/subscriptions_list.html', context)
