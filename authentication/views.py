from django.shortcuts import render, redirect

# general app imports
from django.urls import reverse_lazy  # to redirect back to the previous page after creating a task

# authentication imports
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    template_name = "authentication/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterView(FormView):
    template_name = "authentication/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterView, self).get(*args, **kwargs)


# old views
def login_index(req):
    context = {}
    return render(req, 'authentication/index.html', context)


def login_page(req):
    # print('login pressed')
    return login_index(req)

