import datetime, copy, xmlrpclib, thread, time
from django.db import models
from django.core.cache import cache
from django.contrib.sitemaps import ping_google
from django.contrib.sites.models import Site
from django.dispatch import Signal
from django.db.models import signals
from django.core.mail import mail_admins
from lifeflow.text_filters import entry_markup


class Author(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        help_text="Automatically built from author's name.",
        )
    link = models.CharField(
        max_length=200,
        help_text="Link to author's website.")
    bio = models.TextField(
        blank=True, null=True,
        help_text="Bio of author, written in markdown format."
        )
    picture = models.FileField(
        upload_to="lifeflow/author", blank=True, null=True,
        help_text="Picture of author. For best visual appearance should be relatively small (200px by 200px or so)."
        )
    use_markdown = models.BooleanField(
        default=True,
        help_text="If true body is filtered using MarkDown, otherwise html is expected.",
        )

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return u"/author/%s/" % self.slug

    def latest(self, qty=10):
        return self.entry_set.all().filter(**{'pub_date__lte': datetime.datetime.now()})[:qty]

    def name_with_link(self):
        return u'<a href="%s">%s</a>' % (self.get_absolute_url(), self.name)


class Comment(models.Model):
    entry = models.ForeignKey('Entry')
    parent = models.ForeignKey('Comment', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    webpage = models.CharField(max_length=100, blank=True, null=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    html = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-date',)

    def save(self):
        if self.name == u"name" or self.name == u"":
            self.name = u"anonymous"
        if self.webpage == u"http://webpage" or self.webpage == u"http://":
            # better to check for valid URL
            self.webpage = None
        if self.email == u"email":
            # better to check for valid email address
            self.email = None

        title = self.entry.title
        subject = u"[Comment] %s on %s" % (self.name, self.entry.title)
        body = u"Comment by %s [%s][%s] on %s\n\n%s" % (self.name, self.email, self.webpage, title, self.html)
        mail_admins(subject, body, fail_silently=True)
        super(Comment,self).save()

    def get_absolute_url(self):
        return u"%s#comment_%s" % (self.entry.get_absolute_url(), self.pk)

    def __unicode__(self):
        name = self.name or "Unnamed Poster"
        title = self.entry.title or "Unnamed Entry"
        return u": ".join((name, title))


class Draft(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique_for_date='pub_date',
                            blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    edited = models.BooleanField(default=False)
    use_markdown = models.BooleanField(default=True)
    is_translation = models.BooleanField(default=False)
    send_ping = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    flows = models.ManyToManyField('Flow', blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True, null=True)
    series = models.ManyToManyField('Series', blank=True, null=True)
    authors = models.ManyToManyField('Author', blank=True, null=True)

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return "Untitled Draft"


class CurrentEntryManager(models.Manager):
    def get_query_set(self):
        return super(CurrentEntryManager, self).get_query_set().filter(**{'pub_date__lte': datetime.datetime.now()}).filter(**{'is_translation':False})


class Entry(models.Model):
    title = models.CharField(
        max_length=200,
        help_text='Name of this entry.'
        )
    slug = models.SlugField(
        unique_for_date='pub_date',
        help_text='Automatically built from the title.'
        )
    summary = models.TextField(help_text="One paragraph. Don't add &lt;p&gt; tag.")
    body = models.TextField(
        help_text='Use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown-syntax</a>'
        )
    body_html = models.TextField(blank=True, null=True)
    pub_date = models.DateTimeField(
        help_text='If the date and time combination is in the future, the entry will not be visible until after that moment has passed.'
        )
    use_markdown = models.BooleanField(
        default=True,
        help_text="If true body is filtered using MarkDown++, otherwise no filtering is applied.",
        )
    is_translation = models.BooleanField(
        default=False,
        help_text="Only used to add articles to the translation feed.",
        )
    send_ping = models.BooleanField(
        default=False,
        help_text="If true will ping Google and any sites you have specified on saves."
        )
    allow_comments = models.BooleanField(
        default=True,
        help_text="If true users may add comments on this entry.",
        )
    flows = models.ManyToManyField(
        'Flow', blank=True, null=True,
        help_text="Determine which pages and feeds to show entry on.",
        )
    tags = models.ManyToManyField(
        'Tag', blank=True, null=True,
        help_text="Select tags to associate with this entry.",
        )
    series = models.ManyToManyField(
        'Series', blank=True, null=True,
        help_text='Used to associated groups of entries together under one theme.',
        )
    resources = models.ManyToManyField(
        'Resource', blank=True, null=True,
        help_text='Files or images used in entries. MarkDown links are automatically generated.',
        )
    authors = models.ManyToManyField(
        'Author', blank=True, null=True,
        help_text='The authors associated with this entry.',
        )
    # main manager, allows access to all entries, required primarily for admin functionality
    objects = models.Manager()
    # current manager, does not allow access entries published to future dates
    current = CurrentEntryManager()

    class Meta:
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'
        verbose_name_plural = "entries"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u"/entry/%s/%s/" % (
            self.pub_date.strftime("%Y/%b/%d").lower(),
            self.slug,
            )

    def save(self):
        if self.use_markdown:
            self.body_html = entry_markup(self.body, self)
        else:
            self.body_html = self.body
        if self.send_ping is True: self.ping()
        super(Entry,self).save()

    def ping(self):
        # ping all sites to ping (Ping-O-Matic, etc)
        for site in SiteToNotify.objects.all():
            site.ping()

        # inform Google sitemap has changed
        try:
            ping_google()
        except Exception:
            pass

    def get_next_article(self):
        next =  Entry.current.filter(**{'pub_date__gt': self.pub_date}).order_by('pub_date')
        try:
            return next[0]
        except IndexError:
            return None

    def get_previous_article(self):
        previous =  Entry.current.filter(**{'pub_date__lt': self.pub_date}).order_by('-pub_date')
        try:
            return previous[0]
        except IndexError:
            return None

    def get_random_entries(self):
        return Entry.current.order_by('?')[:3]

    def get_recent_comments(self, qty=3):
        return Comment.objects.all().filter(entry=self)[:qty]

    def organize_comments(self):
        """
        Used to create a list of threaded comments.

        This is a bit tricky since we only know the parent for
        each comment, as opposed to knowing each parent's children.
        """
        def build_relations(dict, comment=None, depth=-1):
            if comment is None: id = None
            else: id = comment.id
            try:
                children = dict[id]
                children.reverse()
                return [(comment, depth), [build_relations(dict, x, depth+1) for x in children]]
            except:
                return (comment, depth)

        def flatten(l, ltypes=(list, tuple)):
            i = 0
            while i < len(l):
                while isinstance(l[i], ltypes):
                    if not l[i]:
                        l.pop(i)
                        if not len(l):
                            break
                    else:
                        l[i:i+1] = list(l[i])
                i += 1
            return l

        def group(seq, length):
            """
            Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/496784
            """
            return [seq[i:i+length] for i in range(0, len(seq), length)]

        dict = {None:[]}
        all = Comment.objects.select_related().filter(entry=self)
        for comment in all:
            if comment.parent: id = comment.parent.id
            else: id = None
            try:
                dict[id].append(comment)
            except KeyError:
                dict[id] = [comment]
        relations = build_relations(dict)
        # If there are no comments, return None
        if len(relations) == 1:
            return None
        # Otherwise, throw away the None node, flatten
        # the returned list, and regroup the list into
        # 2-lists that look like
        #   [CommentInstance, 4]
        # where CommentInstance is an instance of the
        # Comment class, and 4 is the depth of the
        # comment in the layering
        else:
            return group(flatten(relations[1]), 2)


class Flow(models.Model):
    """
    A genre of entries. Like things about Cooking, or Japan.
    Broader than a tag, and gets its own nav link and is available
    at /slug/ instead of /tags/slug/
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField()

    def __unicode__(self):
        return self.title

    def latest(self, qty=None):
        if qty is None:
            return self.entry_set.all().filter(**{'pub_date__lte': datetime.datetime.now()}).filter(**{'is_translation':False})
        else:
            return self.entry_set.all().filter(**{'pub_date__lte': datetime.datetime.now()}).filter(**{'is_translation':False})[:qty]

    def get_absolute_url(self):
        return u"/%s/" % self.slug


class Language(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u"/language/%s/" % self.slug

    def latest(self, qty=None):
        translations = self.translation_set.all().filter(**{'translated__pub_date__lte': datetime.datetime.now()})
        return [ x.translated for x in translations ]


class Project(models.Model):
    """
    A project of any kind. Think of it as a piece in a portfolio.
    """
    title = models.CharField(max_length=50)
    slug = models.SlugField(
        help_text='Automatically built from the title.'
        )
    summary = models.TextField(help_text="One paragraph. Don't add &lt;p&gt; tag.")
    body = models.TextField(
        help_text='Use <a href="http://daringfireball.net/projects/markdown/syntax">Markdown-syntax</a>')
    body_html = models.TextField(blank=True, null=True)
    use_markdown = models.BooleanField(default=True)
    language = models.CharField(
        max_length=50,
        help_text="The programming language the project is written in.",
        )
    license = models.CharField(
        max_length=50,
        help_text="The license under which the project is released.",
        )
    resources = models.ManyToManyField('Resource', blank=True, null=True)
    SIZE_CHOICES = (
        ('0', 'Script'),
        ('1', 'Small'),
        ('2', 'Medium'),
        ('3', 'Large'),
        )
    size = models.CharField(
        max_length=1, choices=SIZE_CHOICES,
        help_text="Used for deciding order projects will be displayed in.",
        )

    class Meta:
        ordering = ('-size',)

    def __unicode__(self):
        return self.title

    def size_string(self):
        if self.size == str(0): return "Script"
        if self.size == str(1): return "Small"
        elif self.size == str(2): return "Medium"
        elif self.size == str(3): return "Large"

    def get_absolute_url(self):
        return u"/projects/%s/" % self.slug

    def save(self):
        if self.use_markdown:
            self.body_html = entry_markup(self.body, self)
        else:
            self.body_html = self.body
        super(Project,self).save()


class Resource(models.Model):
    """
    A wrapper for files (image or otherwise, the model is unaware of the
    distinction) that are used in blog entries.
    """
    title = models.CharField(max_length=50)
    markdown_id = models.CharField(max_length=50)
    content = models.FileField(upload_to="lifeflow/resource")


    def get_relative_url(self):
        # figure out why I named this relative instead of absolute
        # because... it sure as hell isn't relative
        return u"/media/%s" % self.content

    def __unicode__(self):
        return u"[%s] %s" % (self.markdown_id, self.title,)


class RecommendedSite(models.Model):
    """
    A site that is displayed under the 'Blogs-To-See' entry
    on each page of the website. Akin to entries in a blog roll
    on a WordPress blog.
    """
    title = models.CharField(max_length=50)
    url = models.URLField()


    def __unicode__(self):
        return u"%s ==> %s" % (self.title, self.url)


class Series(models.Model):
    """
    A series is a collection of Entry instances on the same theme.
    """
    title = models.CharField(max_length=200)
    slug= models.SlugField()

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = "Series"


    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u"/articles/%s/" % ( unicode(self.slug), )

    def latest(self, qty=10):
        return self.entry_set.all().filter(**{'pub_date__lte': datetime.datetime.now()})[:qty]

    def in_order(self):
        return self.entry_set.order_by('id')

    def num_articles(self):
        return self.entry_set.all().count()


class SiteToNotify(models.Model):
    """
    SiteToNotify instances are pinged by Entries where
    someEntry.ping_sites is True.

    Sites such as 'Ping-O-Matic' are easiest to use here.
    Manually creating the Ping-O-Matic instance looks
    something like this:

    stn = SiteToNotify(title="Ping-O-Matic",
                       url_to_ping="http://rpc.pingomatic.com/",
                       blog_title="My Blog's Title",
                       blog_url="http://www.myblog.com")
    stn.save()
    """
    title = models.CharField(max_length=100)
    url_to_ping = models.CharField(max_length=200)
    blog_title = models.CharField(max_length=100)
    blog_url = models.CharField(max_length=200)


    class Meta:
        verbose_name_plural = "Sites to Notify"


    def __unicode__(self):
        return self.title

    def ping(self):
        def do_ping():
            remote_server = xmlrpclib.Server(self.url_to_ping)
            remote_server.weblogUpdates.ping(self.blog_title, self.blog_url)
        thread.start_new_thread(do_ping, ())


class Tag(models.Model):
    "Tags are associated with Entry instances to describe their contents."
    title = models.CharField(max_length=50)
    slug = models.SlugField()


    class Meta:
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u"/tags/%s/" % self.slug

    def random(self):
        return self.entry_set.all().order_by('?')

    def latest(self, qty=None):
        if qty is None:
            return self.entry_set.all().filter(**{'pub_date__lte': datetime.datetime.now()})
        else:
            return self.entry_set.all().filter(**{'pub_date__lte': datetime.datetime.now()})[:qty]

    def get_max_tags(self):
        max = cache.get('lifeflow_tags_max')
        if max == None:
            tags = Tag.objects.all()
            max = 0
            for tag in tags:
                count = tag.entry_set.count()
                if count > max: max = count
            cache.set('lifeflow_tags_max', max)
        return max

    def tag_size(self):
        max = self.get_max_tags()
        count = self.entry_set.count()
        ratio = (count * 1.0) / max
        tag_name = "size"
        if ratio < .2: return tag_name + "1"
        elif ratio < .4: return tag_name + "2"
        elif ratio < .6: return tag_name + "3"
        elif ratio < .8: return tag_name + "4"
        else: return tag_name + "5"


class Translation(models.Model):
    """
    Link together two entries, where @translated is a translation of
    @original in the language @language.
    """
    language = models.ForeignKey('Language')
    original = models.ForeignKey('Entry')
    translated = models.ForeignKey('Entry', related_name="translated")


    def __unicode__(self):
        return u"Translation of %s into %s" % (self.original, self.language,)


    def get_link(self):
        url = self.translated.get_absolute_url()
        return u'<a href="%s">%s</a>' % (url, self.language,)

    def get_absolute_url(self):
        return self.translated.get_absolute_url()


def resave_object(sender, instance, signal, *args, **kwargs):
    """
    This is called to save objects a second time after required
    manyTomany relationships have been established.

    There must be a better way of handling this.
    """
    def do_save():
        time.sleep(3)
        try:
            instance.save()
        except:
            pass

    id = u"%s%s" % (unicode(instance), unicode(instance.id))
    try:
        should_resave = resave_hist[id]
    except KeyError:
        resave_hist[id] = True
        should_resave = True

    if should_resave is True:
        resave_hist[id] = False
        thread.start_new_thread(do_save, ())
    else:
        resave_hist[id] = True


resave_hist = {}
signals.post_save.connect(resave_object, sender=Project)
signals.post_save.connect(resave_object, sender=Entry)
