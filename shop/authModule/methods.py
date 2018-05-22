from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


def auth_user(request, username, password) -> User:
  user = authenticate(request, username=username, password=password)
  if user is not None:
    login(request, user)

  return user


def is_admin(login_url):
  def check(user):
    if user.is_authenticated:
        if user.is_staff:
          return True
        else:
          raise PermissionDenied()

    return False

  return user_passes_test(check, login_url=login_url)