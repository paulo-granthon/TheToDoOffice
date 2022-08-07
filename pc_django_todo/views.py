from django.shortcuts import render


def close_modal(req):
    return render(req, 'modal.html', {})
