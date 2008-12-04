from django.contrib.syndication.feeds import Feed
from django.conf import settings
from lifeflow.models import *


 
class AllFeed(Feed):
    title = u"%s" % settings.LIFEFLOW_BLOG_NAME 
    link = u"/"
    description = u"The full feed of all entries! Piping hot and ready for consumption."
    copyright = u'Creative Commons License'


    def items(self):
        return Entry.current.all().order_by('-pub_date')[:25]
    
    def item_pubdate(self, item):
        return item.pub_date



class FlowFeed(Feed):
    def get_object(self, bits):
        slug = bits[0]
        return Flow.objects.get(slug=slug)


    def title(self, obj):
        return u"%s: %s" % (settings.LIFEFLOW_BLOG_NAME,
                                              obj.title)


    def link(self, obj):
        return obj.get_absolute_url()


    def description(self, obj):
        return u"The piping hot feed for all entries in the %s flow." % obj.title


    def items(self, obj):
        return obj.latest(qty=25)
    
    def item_pubdate(self, item):
        return item.pub_date



class TagFeed(Feed):
    def get_object(self, bits):
        slug = bits[0]
        return Tag.objects.get(slug=slug)

    
    def title(self, obj):
        return u"%s: the %s tag" % (settings.LIFEFLOW_BLOG_NAME,
                                              obj.title)


    def link(self, obj):
        return obj.get_absolute_url()


    def description(self, obj):
        return u"All entries tagged with %s." % obj.title

    
    def items(self, obj):
        return obj.latest()


    def item_pubdate(self, item):
        return item.pub_date


class AuthorFeed(Feed):
    def get_object(self, bits):
        slug = bits[0]
        return Author.objects.get(slug=slug)


    def title(self, obj):
        return u"%s: %s" % (settings.LIFEFLOW_BLOG_NAME,
                                              obj.name)
    
    def title(self, obj):
        return u"Feed for stuff by %s." % obj.name


    def link(self, obj):
        return obj.get_absolute_url()


    def description(self, obj):
        return u"Recent entries written by %s." % obj.name

    
    def items(self, obj):
        return obj.latest()


    def item_pubdate(self, item):
        return item.pub_date


class LanguageFeed(Feed):
    def get_object(self, bits):
        slug = bits[0]
        return Language.objects.get(slug=slug)


    def title(self, obj):
        return u"%s: %s" % (settings.LIFEFLOW_BLOG_NAME,
                                              obj.title)
    
    def title(self, obj):
        return u"Feed for stuff translated into %s." % obj.title


    def link(self, obj):
        return obj.get_absolute_url()


    def description(self, obj):
        return u"Recent entries translated into %s." % obj.title

    
    def items(self, obj):
        return obj.latest()
    
    
    def item_pubdate(self, item):
        return item.pub_date



class SeriesFeed(Feed):
    def get_object(self, bits):
        slug = bits[0]
        return Series.objects.get(slug=slug)

    
    def title(self, obj):
        return u"%s: %s" % (settings.LIFEFLOW_BLOG_NAME,
                                              obj.title)


    def link(self, obj):
        return obj.get_absolute_url()


    def description(self, obj):
        return u"Entries in the %s series." % obj.title

    
    def items(self, obj):
        return obj.latest()
        
        
    def item_pubdate(self, item):
        return item.pub_date



class TranslationFeed(Feed):
    title = u"%s: Translations" % settings.LIFEFLOW_BLOG_NAME
    link = u"/"
    description = u"Recent translationed entries."
    copyright = u'Creative Commons License'


    def items(self):
        return Entry.objects.all().filter(**{'pub_date__lte': datetime.datetime.now()}).filter(**{'is_translation':True})
    
    
    def item_pubdate(self, item):
        return item.pub_date

class CommentFeed(Feed):
    title = u"%s: Comments" % settings.LIFEFLOW_BLOG_NAME
    link = "/"
    description = u"Latest comments on %s." % settings.LIFEFLOW_BLOG_NAME
    copyright = u'Creative Commons License'
    

    def items(self):
        return Comment.objects.all().order_by('-date',)[:20]
        
    
    def item_pubdate(self, item):
        return item.date



class EntryCommentFeed(Feed):
    def get_object(self, bits):
        year = bits[0]
        month = bits[1]
        day = bits[2]
        slug = bits[3]
        return Entry.objects.get(pub_date__year=year,
                                 pub_date__month=month,
                                 pub_date__day=day,
                                 slug=slug)

    
    def title(self, obj):
        return u"%s: Comments for %s" % (settings.LIFEFLOW_BLOG_NAME,
                                              obj.title)


    def link(self, obj):
        return obj.get_absolute_url()


    def description(self, obj):
        return u"Comments for %s." % obj.title

    
    def items(self, obj):
        return obj.comment_set.all().order_by('-date')
        
    
    def item_pubdate(self, item):
        return item.date
    
