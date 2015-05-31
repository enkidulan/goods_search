"""URL's Dispatching Module. Add any new URL routing here"""
from django.conf.urls import patterns, url
from django.conf import settings
from . import views
from django.http import HttpResponseRedirect

# pylint: disable=invalid-name
urlpatterns = patterns(
    '',
    url(r'^search?', views.search),
    url(r'^$', lambda r: HttpResponseRedirect('index.html')),
    url(r'^(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.FRONTEND_APP_PATH}),
)
