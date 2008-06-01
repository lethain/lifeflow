from django.conf.urls.defaults import *
from lifeflow.feeds import *
from lifeflow.models import *
from lifeflow.sitemaps import ProjectSitemap
from django.contrib.sitemaps import GenericSitemap



flows = Flow.objects.all()

projects = Project.objects.all()

tags = Tag.objects.all().order_by('title')

languages = Language.objects.all()

authors = Author.objects.all().order_by('name')

feeds = {
    'author': AuthorFeed,
    'all' : AllFeed,
    'flow' : FlowFeed,
    'tag' : TagFeed,
    'series' : SeriesFeed,
    'translations' : TranslationFeed,
    'projects' : ProjectFeed,
    'comment' : CommentFeed,
    'entry_comment' : EntryCommentFeed,
    'language' : LanguageFeed,
}

all_dict = {
    'queryset' : Entry.objects.all(),
    'date_field' : 'pub_date',
}

sitemaps = {
    'projects' : ProjectSitemap,
    'entries' : GenericSitemap(all_dict, priority=0.6),
}

urlpatterns = patterns('',
    (r'^$', 'lifeflow.views.front'),

    # sitemap
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # comments
    (r'^comments/create/$', 'lifeflow.views.comments'),
    (r'^comments/create/(?P<entry_id>\d+)/$', 'lifeflow.views.comments'),
    (r'^comments/create/(?P<entry_id>\d+)/(?P<parent_id>\d+)/$', 'lifeflow.views.comments'),

    # feeds and rss views
    (r'^feeds/(?P<url>.*)/$', 
     'django.contrib.syndication.views.feed', 
     {'feed_dict': feeds}),
    (r'^meta/rss/$', 'lifeflow.views.rss'),

    # date based generic views
    (r'^entry/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
     'django.views.generic.date_based.object_detail',
     dict(all_dict, slug_field='slug')),
    (r'^entry/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'django.views.generic.date_based.archive_day',   all_dict),
    (r'^entry/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'django.views.generic.date_based.archive_month', all_dict),
    (r'^entry/(?P<year>\d{4})/$', 'django.views.generic.date_based.archive_year',  all_dict),
    (r'^entry/$', 'django.views.generic.date_based.archive_index', all_dict),

    # tag generic views
    (r'^tags/$', 'django.views.generic.list_detail.object_list', dict(queryset=tags)),
    (r'^tags/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(queryset=tags, slug_field='slug')),

    # language generic views
    (r'^language/$', 'django.views.generic.list_detail.object_list', dict(queryset=languages)),
    (r'^language/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(queryset=languages, slug_field='slug')),

    # author generic views
    (r'^author/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(queryset=authors, slug_field='slug')),
    (r'^author/$', 'django.views.generic.list_detail.object_list', dict(queryset=authors)),

    # articles views (custom view)
    (r'^articles/$', 'lifeflow.views.articles'),

    # projects views
    (r'^projects/$',
     'django.views.generic.list_detail.object_list',
     dict(queryset=projects)),
    (r'^projects/(?P<slug>[-\w]+)/$',
     'django.views.generic.list_detail.object_detail',
     dict(queryset=projects, slug_field='slug')),

    # editor
    (r'^editor/', include('lifeflow.editor.urls')),

    # flows
    (r'^(?P<slug>[-\w]+)/$', 'lifeflow.views.flow'),
)
