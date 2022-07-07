from django.shortcuts import render, redirect


def login_index(req):
    context = {}
    return render(req, 'authentication/index.html', context)


def login_page(req):
    print('login pressed')
    return login_index(req)
