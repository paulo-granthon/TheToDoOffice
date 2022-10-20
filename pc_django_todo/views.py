from django.shortcuts import render


def close_modal(req):
    return render(req, 'modal.html', {})

def switch_theme (req):
    if 'theme' in req.session:
        req.session['theme'] = 'light' if req.session['theme'] == 'dark' else 'dark'
    else: req.session.update({'theme' : 'dark'})
    return render(req, 'theme.html', {'theme' : req.session['theme']})