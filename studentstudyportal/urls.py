"""
URL configuration for studentstudyportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls.conf import include
from dashboard import views as dash_views
from django.contrib.auth import views as auth_views
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('dashboard.urls')), 
    path('register/',dash_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='dashboard/login.html'),name='login'),
    #path('logout/',auth_views.LogoutView.as_view(template_name='dashboard/logout.html'),name='logout'),
    path('logout/',dash_views.logout,name='logout'),
    path('profile/',dash_views.profile,name='profile'),
] + debug_toolbar_urls()

