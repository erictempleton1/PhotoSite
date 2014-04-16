from django.conf.urls import patterns, url

from photo_site import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)