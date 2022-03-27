from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from video.models import Video
from channel.models import Channel
from .forms import UserUpdateForm


def loginView(request):
    if request.user.is_authenticated:
        return redirect("video:index")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("video:index")
        else:
            return render(request, "account/login.html", {
                "error": "Check your username or password!"
            })

    return render(request, "account/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("video:index")

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html",
                              {
                                  "error": "Username is already used.",
                                  "username": username,
                                  "email": email,
                                  "firstname": firstname,
                                  "lastname": lastname
                              })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html",
                                  {
                                      "error": "Email is already used.",
                                      "username": username,
                                      "email": email,
                                      "firstname": firstname,
                                      "lastname": lastname
                                  })
                else:
                    user = User.objects.create_user(
                        username=username, email=email, first_name=firstname, last_name=lastname, password=password)
                    user.save()
                    login(request, user)
                    return redirect("channel:createChannel")
        else:
            return render(request, "account/register.html", {
                "error": "Passwords does not match!",
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname
            })

    return render(request, "account/register.html")


@login_required
def logoutView(request):
    logout(request)
    return redirect("video:index")

# user


@login_required
def userProfile(request):
    if Channel.objects.filter(user_id=request.user.id).exists():
        channel = Channel.objects.get(user=request.user.id)
        context = {
            'channel': channel,
            'total_videos': Video.objects.filter(channel_id=channel.id, user_id=request.user.id).count(),
            'channel': channel,
        }
    else:
        messages.warning(
        request, 'You must create a channel to subscribe channels!')
        return redirect('channel:createChannel')
    return render(request, 'account/user/profile.html', context)


@login_required
def updateUserProfile(request):
    u_form = UserUpdateForm(request.POST, instance=request.user)
    if request.method == 'POST':
        if u_form.is_valid():
            password = request.POST["password"]
            repassword = request.POST["repassword"]

            if password == repassword:
                user = u_form.save()
                messages.success(request, 'Your Profile has been updated!')
                login(request, user)
                return redirect("account:userProfile")
            else:
                return render(request, "account/user/update_profile.html", {
                    "error": "Passwords does not match!",
                    'form': u_form
                })
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {'form': u_form}
    return render(request, 'account/user/update_profile.html', context)
