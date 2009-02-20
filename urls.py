from django.conf.urls.defaults import *
from lifeflow.feeds import *
from lifeflow.models import *
from lifeflow.sitemaps import ProjectSitemap
from django.contrib.sitemaps import GenericSitemap
from django.views.decorators.cache import cache_page
from django.contrib.syndication.views import feed

# Cache
def cache(type):
    return cache_page(type, 60*30)


handler500 = 'lifeflow.views.server_error'

flows = Flow.objects.all()
projects = Project.objects.all()
tags = Tag.objects.all()
languages = Language.objects.all()
authors = Author.objects.all()

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

urlpatterns = patterns(
    '',
    url(r'^$', 'lifeflow.views.front'),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    # comments
    url(r'^comments/create/$', 'lifeflow.views.comments'),
    url(r'^comments/create/(?P<entry_id>\d+)/$', 'lifeflow.views.comments'),
    url(r'^comments/create/(?P<entry_id>\d+)/(?P<parent_id>\d+)/$', 'lifeflow.views.comments'),

    # feeds and rss views
    url(r'^feeds/(?P<url>.*)/$', cache(feed), {'feed_dict': feeds}),
    url(r'^meta/rss/$', 'lifeflow.views.rss'),

    # date based generic views
    url(r'^entry/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$', 'django.views.generic.date_based.object_detail', dict(all_dict, slug_field='slug')),
    url(r'^entry/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 'django.views.generic.date_based.archive_day',   all_dict),
    url(r'^entry/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'django.views.generic.date_based.archive_month', all_dict),
    url(r'^entry/(?P<year>\d{4})/$', 'django.views.generic.date_based.archive_year',  all_dict),
    url(r'^entry/$', 'django.views.generic.date_based.archive_index', all_dict),

    # tag generic views
    url(r'^tags/$', 'django.views.generic.list_detail.object_list', dict(queryset=tags)),
    url(r'^tags/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(queryset=tags, slug_field='slug')),

    # language generic views
    url(r'^language/$', 'django.views.generic.list_detail.object_list', dict(queryset=languages)),
    url(r'^language/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(queryset=languages, slug_field='slug')),

    # author generic views
    url(r'^author/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(queryset=authors, slug_field='slug')),
    url(r'^author/$', 'django.views.generic.list_detail.object_list', dict(queryset=authors)),

    # articles views (custom view)
    url(r'^articles/$', 'lifeflow.views.articles'),

    # projects views
    url(r'^projects/$', 'django.views.generic.list_detail.object_list', dict(queryset=projects)),
    url(r'^projects/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(queryset=projects, slug_field='slug')),

    # editor
    url(r'^editor/', include('lifeflow.editor.urls')),

    # flows
    url(r'^(?P<slug>[-\w]+)/$', 'lifeflow.views.flow'),
)
