from django.shortcuts import render


def login_requireds(request):
    return render(request,'loginrequired.html')
