from django.conf.urls.defaults import *
from lifeflow.models import *

urlpatterns = patterns('lifeflow.editor.views',
    (r'^$', 'overview'),
    (r'^comments/$', 'comments'),
    (r'^blogroll/$', 'blogroll'),
    (r'^files/$', 'files'),

    (r'^authors/$', 'authors'),
    (r'^authors/create/$', 'create_author'),
    (r'^authors/(?P<id>\d+)/$', 'author_edit'),
    (r'^authors/(?P<id>\d+)/create/$', 'create_author'),

    (r'^projects/$', 'projects'),
    (r'^projects/create/$', 'create_project'),
    (r'^projects/(?P<id>\d+)/details/$','project_details'),
    (r'^projects/(?P<id>\d+)/body/$','project_body'),

    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),

    (r'^create/$', 'create'),
    (r'^update/$', 'update'),
    (r'^display_resource/(?P<id>\d+)/$', 'display_resource'),
    (r'^add_resource/', 'add_resource'),
    (r'^display_author/(?P<id>\d+)/$', 'display_author'),
    (r'^add_author_picture/', 'add_author_picture'),
    (r'^create_model/', 'create_model'),
    (r'^delete_model/', 'delete_model'),

    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/1/$', 'edit_one'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/2/$', 'edit_two'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/3/$', 'edit_three'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/4/$', 'edit_four'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/5/$', 'edit_five'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/6/$', 'edit_six'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/7/$', 'edit_seven'),
    (r'^rough_to_edited/(?P<id>\d+)/$', 'rough_to_edited'),
    (r'^edited_to_rough/(?P<id>\d+)/$', 'edited_to_rough'),
    (r'^edited_to_published/(?P<id>\d+)/$', 'edited_to_published'),
    (r'^published_to_edited/(?P<id>\d+)/$', 'published_to_edited'),
    (r'^render/(?P<model>\w+)/(?P<id>\d+)/$', 'render'),
    (r'^render/$', 'render'),
)
