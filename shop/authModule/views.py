from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from shop.forms import UserLoginForm, UserRegisterForm


class UserLogin(View):
  template_name = 'login.html'

  def get(self, request):
    if request.user.is_authenticated:
      return redirect(reverse_lazy('home'))

    return render(request, self.template_name, {'form': UserLoginForm()})

  def post(self, request):
    if request.user.is_authenticated:
      return redirect(reverse_lazy('home'))

    form = UserLoginForm(request)
    if not form.is_valid():
      return render_to_response(self.template_name, {'form': form})

    if request.GET.get('next'):
      return HttpResponseRedirect(request.GET.get('next'))

    return redirect(reverse_lazy('home'))


class UserLogout(View):
  def get(self, request):
    logout(request)
    return redirect(reverse_lazy('home'))

  def post(self, request):
    return HttpResponse("Post is not allowed")


class UserRegister(CreateView):
  template_name = 'register.html'
  model = User
  form_class = UserRegisterForm
  success_url = reverse_lazy('home')

  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect(reverse_lazy('home'))

    return super(UserRegister, self).get(request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect(reverse_lazy('home'))

    return super(UserRegister, self).post(request, *args, **kwargs)