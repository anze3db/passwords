from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
    (r'^admin/', include(admin.site.urls)),
    (r'^add/', 'web.views.add'),
    (r'^id/(\d+)', 'web.views.id'),    
    (r'^$', 'web.views.index'),
)
