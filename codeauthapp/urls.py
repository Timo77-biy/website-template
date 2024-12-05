"""
URL configuration for morningDjangoHtmlFormsProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views
from codeauthapp import views
from .views import logout, custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/',custom_logout, name='custom-logout'),

    path('token', views.token, name='token'),
    path('pay', views.pay, name='pay'),
    path('stk', views.stk, name="stk"),

    path('', user_views.index, name='home-page'),
    path('contact/', user_views.contact, name='contact us'),
    path('about/',user_views.about, name='my_about'),
    path('register/', user_views.register, name='user-registration'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='user-login'),
    path('shop/', user_views.shop, name='shop'),
    path('pay', user_views.pay, name='pay'),

]