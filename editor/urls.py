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

    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/title/$', 'article_title'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/body/$', 'article_body'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/flows/$', 'article_flows'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/tags/$', 'article_tags'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/series/$', 'article_series'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/options/$', 'article_options'),
    (r'^edit/(?P<category>\w+)/(?P<id>\d+)/authors/$', 'article_authors'),
    (r'^rough_to_edited/(?P<id>\d+)/$', 'rough_to_edited'),
    (r'^edited_to_rough/(?P<id>\d+)/$', 'edited_to_rough'),
    (r'^edited_to_published/(?P<id>\d+)/$', 'edited_to_published'),
    (r'^published_to_edited/(?P<id>\d+)/$', 'published_to_edited'),
    (r'^render/(?P<model>\w+)/(?P<id>\d+)/$', 'render'),
    (r'^render/$', 'render'),
)
