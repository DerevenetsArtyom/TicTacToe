from django.conf.urls import url


urlpatterns = [
    url(r'^home$', 'user_profile.views.home', name='user_home')
]