from django.conf.urls import url
from django.urls import reverse_lazy

from shop.authModule.views import UserLogin, UserRegister, UserLogout

login_url = reverse_lazy('login')

urlpatterns = [
  url(r'^login$', UserLogin.as_view(),
      name="login"),

  url(r'^register$', UserRegister.as_view(),
      name="register"),

  url(r'^logout$', UserLogout.as_view(),
      name="logout"),
]