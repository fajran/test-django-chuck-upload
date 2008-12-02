from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^upload/(\d+)/', 'upload.handler.upload_chunk'),
    (r'^upload/', 'upload.handler.upload_request'),

	(r'^test/request/', 'upload.testupload.request'),
	(r'^test/chunk/(\d+)/', 'upload.testupload.chunk'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
