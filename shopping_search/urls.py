from django.conf.urls import patterns, url
from django.conf import settings
from . import views
from django.http import HttpResponseRedirect

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    # search request
    url(r'^search?', views.search),
    url(r'^item?', views.item),
    url(r'^$', lambda r: HttpResponseRedirect('index.html')),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.FRONTEND_APP_PATH}),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )