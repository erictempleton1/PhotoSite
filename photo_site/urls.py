from django.conf.urls import patterns, url

from photo_site import views

urlpatterns = patterns('',
    #url(r'^$', views.test_layout, name='test_layout'),
    #url(r'^(?P<user_id>\d+)/home/$', views.user_page, name='user_page'),
    #url(r'^$', views.index, name='index'),
    url(r'^photos/$', views.index, name='index'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^signup/$', views.signup, name='signup'),
)