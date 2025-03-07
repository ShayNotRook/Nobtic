from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.conf import settings

static_url = settings.STATIC_URL


class Login(LoginView):
    template_name = f'registration/login.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        repsonse = super().form_valid(form)
        return redirect('scheduler:apps')