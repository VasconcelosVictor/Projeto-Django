
from django import contrib
from django.conf.urls import url
from django.contrib import admin
from django.urls import path , include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('tasks.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

]
