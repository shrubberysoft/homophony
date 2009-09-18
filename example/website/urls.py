from django.conf.urls.defaults import *

urlpatterns = patterns('example.website.views',
    (r'^$', 'home'),
    (r'^hello$', 'say_hello'),
)
