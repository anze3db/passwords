from django.conf.urls.defaults import *

urlpatterns = patterns('web.views',    
    (r'^add/', 'add'),
    (r'^$', 'index'),
)