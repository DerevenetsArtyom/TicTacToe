from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.home', name='boardgames_home'),
    url(r'^user/', include('user_profile.urls')),

    # Default Login / Logout
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='boardgames_login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'boardgames_home'}, name='boardgames_logout'),
]

