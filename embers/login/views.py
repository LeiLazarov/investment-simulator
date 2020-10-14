from django.shortcuts import render, redirect

from login import models


def index(request):
    return render(request, 'index.html')


def login(request):
    # if request.session.get('is_login', None):
    #     return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = 'check input contents'
        if username.strip() and password.strip():
            try:
                user = models.User.objects.get(username=username)
            except:
                message = 'username does not exist!'
                return render(request, 'login/login.html', {'message': message})
            if user.password == password:
                # request.session['is_login'] = True
                # request.session['user_id'] = user.id
                # request.POST.session['user_name'] = user.username
                return redirect('/')
            else:
                message = 'incorrect password'
                return render(request, 'login/login.html', {'message': message})
        else:
            return render(request, 'login/login.html', {'message': message})
    return render(request, 'login/login.html')


def registration(request):
    if request.method == 'POST':
        message = 'check input content'
        username = request.POST.get('username')
        password_01 = request.POST.get('password_01')
        password_02 = request.POST.get('password_02')
        if username.strip() and password_01.strip() and password_02.strip():
            if password_01 != password_02:
                message = 'two passwords are different'
                return render(request, 'login/registration.html', {'message': message})
            else:
                same_username = models.User.objects.filter(username=username)
                if same_username:
                    message = 'username already exists'
                    return render(request, 'login/registration.html', {'message': message})
                new_user = models.User()
                new_user.username = username
                new_user.password = password_01
                new_user.save()
                return redirect('/login/')
    return render(request, 'login/registration.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/login/')


