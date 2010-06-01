from django.conf.urls.defaults import *

urlpatterns = patterns('sample.website.views',
    (r'^$', 'home'),
    (r'^hello$', 'say_hello'),
)
