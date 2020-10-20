from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, SettingsForm, ProfilePicForm
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile


def signUpUser(request):
    context = dict()
    url = request.META.get('HTTP_REFERER')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password == confirm:
            if User.objects.filter(username=username).exists():
                print("Username taken ")
                context['username'] = "Bu kullanıcı Adı daha önce alınmış."
                messages.warning(request, "Bu kullanıcı Adı daha önce alınmış")

                return redirect(url, context)

            elif User.objects.filter(email=email).exists():
                print("Email taken ")
                context['email'] = "Bu email daha önce kullanılmış."
                messages.warning(request, "Bu email daha önce kullanılmış.")

                return redirect(url, context)
            else:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()

                messages.warning(request, "Başarılı bir şekilde kayıt oldunuz.")
                return redirect('login')
        else:
            print('Password not matching.. ')
    else:

        context['form'] = form

        return render(request, 'register.html', context)


def loginUser(request):
    context = dict()

    form = LoginForm(request.POST or None)
    print(form)
    context['form'] = form

    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        print(email)
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None:
            messages.info(request, 'Username or Password Wrong ')
            return render(request, 'login.html', context)

        messages.success(request, 'Login Successful')
        login(request, user)
        return redirect('home')

    return render(request, 'login.html', context)


def logoutUser(request):
    context = dict()

    logout(request)
    message = messages.success(request, 'Exit Successful')

    context['form'] = message

    return redirect('/', context)

def settings(request):
    context = dict()
    url = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=request.user)
        context['error'] = form.errors
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            return render(request, 'user/failed.html', context)
    else:
        form = SettingsForm(instance=request.user)
        context['form'] = form

    return render(request, 'user/settings.html', context)


def change_password(request):
    context = dict()

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        context['error'] = form.errors
        if form.is_valid():
            form.save()
            print(form)
            update_session_auth_hash(request, form.user)
            return redirect('success')
        else:
            return render(request, 'user/failed.html', context)
    else:
        form = PasswordChangeForm(user=request.user)
        context['form'] = form

        return render(request, 'user/change_password.html', context)


def change_profile_picture(request):
    current_user = request.user
    if request.method == 'POST':
        photo = Profile.objects.get(user_id=current_user.id)
        photo.profile_pic = request.FILES.get('images')
        photo.save()
        return redirect('home')
    return render(request, 'user/profile-picture.html')

def failed(request):
    return render(request, 'user/failed.html')

def success(request):
    return render(request, 'user/success.html')