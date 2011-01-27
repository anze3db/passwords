from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
                       
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^admin/web/password/batch/', 'web.views_admin.batch'),
    (r'^admin/', include(admin.site.urls)),
    (r'^add/', 'web.views.add'),
    (r'^id/(\d+)', 'web.views.id'),  
    (r'^$', 'web.views.index'),  
)
