from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from video.models import Video
from channel.models import Channel
from .forms import UserUpdateForm, ChangeUserPasswordForm


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


def signUp(request):
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
                return render(request, "account/sign_up.html",
                              {
                                  "error": "Username is already used!",
                                  "username": username,
                                  "email": email,
                                  "firstname": firstname,
                                  "lastname": lastname
                              })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/sign_up.html",
                                  {
                                      "error": "Email is already used!",
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
            return render(request, "account/sign_up.html", {
                "error": "Passwords does not match!",
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname
            })

    return render(request, "account/sign_up.html")


@login_required
def logoutView(request):
    logout(request)
    return redirect("account:login")

# user


@login_required
def userProfile(request):
    if Channel.objects.filter(user_id=request.user.id).exists():
        channel = Channel.objects.get(user=request.user.id)
        context = {
            'channel': channel,
            'total_videos': Video.objects.filter(channel_id=channel.id, user_id=request.user.id).count(),
        }
        return render(request, 'account/user/profile.html', context)
    context = {}
    return render(request, 'account/user/profile.html', context)


@login_required
def updateUserProfile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('account:userProfile')
        else:
            return render(request, 'account/update_profile.html', {'form': user_form})

    user_form = UserUpdateForm(instance=request.user)
    return render(request, 'account/update_profile.html', {'form': user_form})

@login_required 
def changeUserPassword(request):

    form = ChangeUserPasswordForm(data=request.POST, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            user = authenticate(request, username=request.user.username, password=form.new_password2)
            login(request, user)
            messages.success(
                request, 'Your password has been successfully updated.')
            return redirect("account:userProfile")

    context = {
        'form': form
    }
    return render(request, 'account/change_password.html', context)
