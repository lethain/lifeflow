from django.conf.urls.defaults import *

from django.conf.urls.defaults import *
from django.conf import settings

from lifeflow.urls import handler500

urlpatterns = patterns(
    '',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    (r'^admin/', include('django.contrib.admin.urls')),
    (r'^', include('lifeflow.urls')),
)
