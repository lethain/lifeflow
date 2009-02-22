"""


TODO

- write function to check a Draft for missing requirements before
  transformation into an Entry, and report that data when the
  transformation fails, instead of just "It failed" msg
- File upload functionality
- Setting datetime
- display list of files in zipfile resources
- display code for code resources


"""


import datetime, os.path, time, re
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponseServerError
from lifeflow.models import *
from lifeflow.text_filters import entry_markup
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import views, authenticate
from django.core.paginator import QuerySetPaginator
from django.contrib.sites.models import Site

from pygments import highlight
from pygments.util import ClassNotFound
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_for_filename

from zipfile import ZipFile

CHARACTERS_TO_STRIP = re.compile(r"[ \.,\!\?'\";:/\\+=#]+")
def sluggify(str):
    return CHARACTERS_TO_STRIP.subn(u"-", str.lower())[0].strip("-")


def login(request):
    error_msg = u""
    if request.method == "POST":
        POST = request.POST.copy()
        username = POST.get('username',"")
        password = POST.get('password',"")

        if username == "" or password == "":
            error_msg = u"Your username AND password, si vous plait."
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect("/editor/")
            else:
                error_msg = u"It works better when the username and password match."
    return render_to_response("lifeflow/editor/login.html",
                              
                              {"login_screen":True,
                               'error_message':error_msg})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")

@login_required
def overview(request):
    rough = Draft.objects.filter(edited=False)
    edited = Draft.objects.filter(edited=True)
    published = Entry.objects.all()
    return render_to_response('lifeflow/editor/overview.html',
                              {'rough':rough,
                               'edited':edited,
                               'published':published},
                              RequestContext(request, {}))

@login_required
def comments(request):
    try:
        page = int(request.GET["page"])
    except:
        page = 1
    page = QuerySetPaginator(Comment.objects.all(), 5).page(page)
    return render_to_response('lifeflow/editor/comments.html',
                              {'page':page},
                              RequestContext(request,{}))

@login_required
def blogroll(request):
    blogroll = RecommendedSite.objects.all()
    return render_to_response('lifeflow/editor/blogroll.html',
                              {'blogroll':blogroll},
                              RequestContext(request,{}))

@login_required
def sites_to_notify(request):
    sites = SiteToNotify.objects.all()
    return render_to_response('lifeflow/editor/sites_to_ping.html',
                              {'sites_to_notify':sites},
                              RequestContext(request,{}))

@login_required
def site_config(request):
    site = Site.objects.get_current()
    return render_to_response('lifeflow/editor/site.html',
                              {'sites_to_notify':site},
                              RequestContext(request,{}))

@login_required
def files(request):
    resources = Resource.objects.all()
    return render_to_response('lifeflow/editor/files.html',
                              {'resources':resources},
                              RequestContext(request,{}))

@login_required
def projects(request):
    projects = Project.objects.all()
    return render_to_response('lifeflow/editor/projects.html',
                              {'projects':projects},
                              RequestContext(request,{}))

@login_required
def project_details(request, id):
    project = Project.objects.get(pk=id)
    return render_to_response('lifeflow/editor/project_details.html',
                              {'object':project},
                              RequestContext(request,{}))

@login_required
def project_body(request, id):
    project = Project.objects.get(pk=id)
    resources = Resource.objects.all()
    return render_to_response('lifeflow/editor/project_body.html',
                              {'object':project,
                               'resources':resources},
                              RequestContext(request,{}))

@login_required
def authors(request):
    authors = Author.objects.all()
    selected = len(authors)-1
    author = authors[selected]
    return render_to_response('lifeflow/editor/authors.html',
                              {'author':author,
                               'authors':authors,
                               'selected':selected},
                              RequestContext(request,{}))

@login_required
def author_edit(request,id):
    author = Author.objects.get(pk=id)
    return render_to_response('lifeflow/editor/author.html',
                              {'author':author},
                              RequestContext(request,{}))

    
    


BOOLEAN_FIELDS = ["send_ping", "allow_comments", "use_markdown"]
MANY_TO_MANY_FIELDS = ["flows", "tags", "series", "authors"]
SLUG_FIELDS = ["slug"]
DATETIME_FIELDS = ["pub_date"]

@login_required
def update(request):
    dict = request.POST.copy()
    id = dict.pop('pk')[0]
    model = dict.pop('model')[0]
    object = get_class(model).objects.get(pk=id)
    obj_dict = object.__dict__
    for key in dict.keys():
        if obj_dict.has_key(key):
            val = dict[key]
            if key in BOOLEAN_FIELDS:
                if val == u"true":
                    val = True
                elif val == u"false":
                    val = False
            elif key in SLUG_FIELDS:
                val = sluggify(val)
            elif key in DATETIME_FIELDS:
                t = time.mktime(time.strptime(val, "%Y-%m-%d %H:%M:%S"))
                val = datetime.datetime.fromtimestamp(t)
            obj_dict[key] = val
        elif key in MANY_TO_MANY_FIELDS:
            vals = dict.getlist(key)
            manager = getattr(object, key)
            manager.clear()
            if not (len(vals) == 1 and int(vals[0]) == -1):
                manager.add(*vals)
    object.save()
    return HttpResponse("success")


API_CLASSES = {"comment":Comment, "project":Project, "flow":Flow, "tag":Tag, "series":Series, "draft":Draft, "entry":Entry, "author":Author, "resource":Resource, "recommendedsite":RecommendedSite,'site_to_notify':SiteToNotify,'site':Site,"language":Language}

def get_class(str):
    return API_CLASSES[str]

@login_required
def delete_model(request):
    cls = get_class(request.POST['model'])
    pk = request.POST['pk']
    try:
        cls.objects.get(pk=pk).delete()
        return HttpResponse("success")
    except:
        return HttpResponseServerError(u"fail")
        

@login_required
def create_model(request):
    def unique(slug, model):
        if model.objects.filter(slug=slug).count() == 0:
            return True
        return False
    toReturn = HttpResponseRedirect(request.META['HTTP_REFERER'])
    model = request.POST['model']
    if model in [u"flow", u"tag", u"series"]:
        cls = get_class(model)
        title = request.POST[u'title']
        slug = sluggify(title)
        if unique(slug, cls):
            f = cls(title=title, slug=slug)
            f.save()
    elif model == u"language":
        title = request.POST[u'title']
        slug = sluggify(title)
        l = Language(title=title,slug=slug)
        l.save()
    elif model == u"site_to_notify":
        title = request.POST[u'title']
        url_to_ping = request.POST[u'url_to_ping']
        blog_title = request.POST[u'blog_title']
        blog_url = request.POST[u'blog_url']
        s = SiteToNotify(title=title,url_to_ping=url_to_ping,blog_title=blog_title,blog_url=blog_url)
        s.save()
    elif model == u"translation":
        translated_pk = int(request.POST[u'pk'])
        translated = Entry.objects.get(pk=translated_pk)
        original_pk = int(request.POST[u'original'])
        language_pk = int(request.POST[u'language'])
        if original_pk == -1 or language_pk == -1:
            [ x.delete() for x in Translation.objects.filter(original=translated)]
            [ x.delete() for x in Translation.objects.filter(translated=translated)]
        else:
            original = Entry.objects.get(pk=original_pk)
            language = Language.objects.get(pk=language_pk)
            
            t = Translation(language=language,original=original,translated=translated)
            t.save()
        # update toReturn to return rendered template of translations
        translations = Translation.objects.filter(translated=translated)
        toReturn = render_to_response('lifeflow/editor/translations.html',
                                      {'translations':translations},
                                      RequestContext(request, {}))

    elif model == u"recommendedsite":
        title = request.POST[u'title']
        url = request.POST[u'url']
        f = RecommendedSite(title=title, url=url)
        f.save()

    return toReturn

@login_required
def add_author_picture(request):
    id = request.POST['pk']
    file = request.FILES['file']
    filename = file.name
    filebase = '%s/lifeflow/author/' % settings.MEDIA_ROOT
    filepath = "%s%s" % (filebase, filename)
    while (os.path.isfile(filepath)):
        filename = "_%s" % filename
        filepath = "%s%s" % (filebase, filename)
    fd = open(filepath, 'wb')
    fd.write(file.read())
    fd.close()
    
    author = Author.objects.get(pk=id)
    author.picture = "lifeflow/author/%s" % filename
    author.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def display_author(request, id):
    pass

@login_required
def add_resource(request):
    file = request.FILES['file']
    title = request.POST['title']
    markdown_id = request.POST['markdown_id']
    filename = file.name
    filebase = '%s/lifeflow/resource/' % settings.MEDIA_ROOT
    filepath = "%s%s" % (filebase, filename)
    while (os.path.isfile(filepath)):
        filename = "_%s" % filename
        filepath = "%s%s" % (filebase, filename)
    fd = open(filepath, 'wb')

    fd.write(file.read())
    fd.close()
    rec = Resource(title=title, markdown_id=markdown_id, content="lifeflow/resource/%s" % filename)
    rec.save()
    id = request.POST['pk']
    model = request.POST['model']
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    #return HttpResponseRedirect("/editor/edit/%s/%s/2/" % (model, id))


IMAGE_EXTS = ["jpg", "jpeg", "png", "gif"]
ZIP_EXTS = ["zip"]
CODE_EXTS = ["css", "html", "htm", "c", "o", "py", "lisp", "js", "xml",
             "java", "rb"]

@login_required
def display_resource(request, id):
    res = Resource.objects.get(pk=id)
    file = res.content.path.split("/")[-1]
    opts = {'object':res,'file':file}
    ext = opts['file'].split(".")[-1]
    opts['type'] = 'file'
    if ext in IMAGE_EXTS:
        opts['type'] = "image"
    elif ext in ZIP_EXTS:
        try:
            opts['type'] = "zip"
            zf = ZipFile(res.content.path,'r')
            opts['files_list'] = zf.namelist()
            zf.close()
        except IOError:
            opts['type'] = "file"
    else:
        try:
            lexer = get_lexer_for_filename(file)
            f = open(res.content.path,'r')
            data = f.read()
            f.close()
            opts['highlighted_code'] = highlight(data,lexer,HtmlFormatter())
            opts['type'] = "code"
        except ClassNotFound:
            opts['type'] = "file"
        except IOError:
            opts['type'] = "file"

    return render_to_response('lifeflow/editor/resource.html',opts,RequestContext(request, {}))


@login_required
def article_title(request, category, id):
    if category == "entry":
        obj = Entry.objects.get(pk=id)
    else:
        obj = Draft.objects.get(pk=id)
    return render_to_response('lifeflow/editor/article_title.html',
                              {'object':obj,
                               'model':category},
                              RequestContext(request, {}))

@login_required
def article_body(request, category, id):
    resources = Resource.objects.all()
    if category == "entry":
        obj = Entry.objects.get(pk=id)
    else:
        obj = Draft.objects.get(pk=id)
    return render_to_response('lifeflow/editor/article_body.html',
                              {'object':obj,
                               'resources':resources,
                               'model':category},
                              RequestContext(request, {}))

@login_required
def article_flows(request, category, id):
    if category == "entry":
        obj = Entry.objects.get(pk=id)
    else:
        obj = Draft.objects.get(pk=id)
    obj_flows = obj.flows.all()
    flows = [ (x, x in obj_flows) for x in Flow.objects.all()] 
    return render_to_response('lifeflow/editor/article_flows.html',
                              {'object':obj,
                               'flows':flows,
                               'model':category},
                              RequestContext(request, {}))

@login_required
def article_tags(request, category, id):
    if category == "entry":
        obj = Entry.objects.get(pk=id)
    else:
        obj = Draft.objects.get(pk=id)
    obj_tags = obj.tags.all()
    tags = [ (x, x in obj_tags) for x in Tag.objects.all()]
    return render_to_response('lifeflow/editor/article_tags.html',
                              {'object':obj,
                               'tags':tags,
                               'model':category},
                              RequestContext(request, {}))

@login_required
def article_series(request, category, id):
    if category == "entry":
        obj = Entry.objects.get(pk=id)
    else:
        obj = Draft.objects.get(pk=id)
    obj_series = obj.series.all()
    series = [ (x, x in obj_series) for x in Series.objects.all()]
    return render_to_response('lifeflow/editor/article_series.html',
                              {'object':obj,
                               'series':series,
                               'model':category},
                              RequestContext(request, {}))


@login_required
def article_options(request, category, id):
    if category == "entry":
        obj = Entry.objects.get(pk=id)
    else:
        obj = Draft.objects.get(pk=id)
    return render_to_response('lifeflow/editor/article_options.html',
                              {'object':obj,
                               'model':category},
                              RequestContext(request, {}))


@login_required
def article_authors(request, category, id):
    if category == "entry":
        obj = Entry.objects.get(pk=id)
    else:
        obj = Draft.objects.get(pk=id)
    obj_authors = obj.authors.all()
    authors = [ (x, x in obj_authors) for x in Author.objects.all()]
    langs = Language.objects.all()
    entries = Entry.objects.all()
    translations = Translation.objects.filter(translated=obj)
    return render_to_response('lifeflow/editor/article_authors.html',
                              {'object':obj,
                               'authors':authors,
                               'langs':langs,
                               'entries':entries,
                               'translations':translations,
                               'model':category},
                              RequestContext(request, {}))



@login_required
def rough_to_edited(request, id):
    try:
        obj = Draft.objects.get(pk=id)
        obj.edited = True
        obj.save()
        return HttpResponse(u"%s" % obj.pk)
    except:
        return HttpResponseServerError(u"Failed.")

@login_required
def edited_to_rough(request, id):
    try:
        obj = Draft.objects.get(pk=id)
        obj.edited = False
        obj.save()
        return HttpResponse(u"%s" % obj.pk)
    except:
        return HttpResponseServerError(u"Failed.")

@login_required
def edited_to_published(request, id):
    def check(dict):
        complaints = []
        if dict[u"title"] in [None, u""]:
            complaints.append("You need to give the entry a title first.")
        if dict[u"body"] in [None, u""]:
            complaints.append("You'll need to fill out the article a bit before publishing it.")          
        if complaints == []:
            return True
        else:
            return "\n<br>\n".join(complaints)

    def transform(draft):
        dict = draft.__dict__.copy()
        del dict['id']
        if dict['pub_date'] is None:
            dict['pub_date'] = datetime.datetime.now()
        del dict['edited']
        if dict['slug'] is None and dict['title'] is not None:
            dict['slug'] = sluggify(dict['title'])
        entry = Entry(**dict)
        valid = check(entry.__dict__)
        if valid != True:
            return None, valid
        else:
            entry.save()
            for field in MANY_TO_MANY_FIELDS:
                getattr(entry, field).add(*getattr(draft, field).all())
            return entry, True

    try:
        draft = Draft.objects.get(pk=id)
        entry, result = transform(draft)
        if result == True:
            draft.delete()
            return HttpResponse(u"%s" % entry.pk)
        else:
            return HttpResponseServerError(result)
    except TypeError:
        return HttpResponseServerError(u"The draft is missing required fields.")
    except:
        return HttpResponseServerError(u"The update made it to the server, but failed for unknown reasons.")

@login_required
def published_to_edited(request, id):
    def transform(entry):
        dict = entry.__dict__.copy()
        dict['edited'] = True
        del dict['body_html']
        del dict['id']
        draft = Draft(**dict)
        draft.save()
        for field in MANY_TO_MANY_FIELDS:
                getattr(draft, field).add(*getattr(entry, field).all())
        return draft
    try:
        entry = Entry.objects.get(pk=id)
        draft = transform(entry)
        entry.delete()
        return HttpResponse(u"%s" % draft.pk)
    except:
        return HttpResponseServerError(u"Update failed.")


@login_required
def create(request):
    obj = Draft()
    obj.save()
    return HttpResponseRedirect("../edit/draft/%s/title/" % obj.pk)

@login_required
def create_project(request):
    obj = Project()
    obj.save()
    return HttpResponseRedirect("/editor/projects/%s/details/" % obj.pk)

@login_required
def create_author(request,id=None):
    obj = Author()
    obj.save()
    return HttpResponseRedirect("/editor/authors/")
    

@login_required
def render(request, model=None, id=None):
    if id is None and request.POST.has_key('pk'):
        id = request.POST['pk']

    if id is None:
        txt = entry_markup(request.POST['txt'])
    else:
        if model == u"draft":
            obj = Draft.objects.get(pk=id)
        elif model ==u"entry":
            obj = Entry.objects.get(pk=id)
        elif model == u"project":
            obj = Project.objects.get(pk=id)
        if obj.use_markdown:
            txt = entry_markup(obj.body, obj)
        else:
            txt = obj.body
    return HttpResponse(txt)
