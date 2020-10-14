from django.shortcuts import render, redirect

def intro(request):
    return render(request, 'tutorial/intro.html')


