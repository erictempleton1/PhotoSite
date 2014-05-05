from django.conf.urls import patterns, url

from photo_site import views

urlpatterns = patterns('',
    #url(r'^$', views.test_layout, name='test_layout'),
    #url(r'^(?P<user_id>\d+)/home/$', views.user_page, name='user_page'),
    url(r'^$', views.index, name='index'),
    url(r'^$', views.test_layout, name='test_layout'),
    url(r'^(?P<username>\w+)/photos/$', views.user_page, name='user_page'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^upload/$', views.upload_image, name='upload_image'),
    url(r'^(?P<username>\w+)/photos/(?P<items_id>\d+)$', views.image_page, name='image_page'),
    url(r'^(?P<test_string>\w+)/$', views.test_view, name='test_view'),
)