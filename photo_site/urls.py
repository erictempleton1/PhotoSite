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
    url(r'^update/$', views.update_image, name='update_image'),
    url(r'^remove/(?P<image_id>\d+)/(?P<image_url>\w+)', views.remove_image, name='remove_image'),

    # might need to adjust this as more admin features are added
    url(r'^user-admin/$', views.change_pw, name='change_pw'),

    # password reset urls
    url(r'^user/password/reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    (r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete'),
)