"""
Views.py

Author: Will Larson
Contact: lethain@gmail.com


Contains one custom view for displaying articles.
Mostly necessary to presort the articles in order
of descending size.

"""
import datetime, time, random, cgi, md5
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.core.paginator import QuerySetPaginator
from lifeflow.models import Series, Flow, Entry, Comment
from lifeflow.forms import CommentForm


def server_error(request):
    return render_to_response('500.html',{},RequestContext(request,{}))


def articles(request):       
    object_list = Series.objects.all()
    return render_to_response('lifeflow/articles.html', {'object_list' : object_list},RequestContext(request, {}))


def comments(request, entry_id=None, parent_id=None):
    def make_identifier(id, time):
        secret = getattr(settings, 'SECRET_KEY')
        time = time[:-4]
        data = "%s%s%s%s" % ("lifeflow", id, time, secret)
        return md5.md5(data).hexdigest()

    # if an entry ID has been posted, use that
    if request.POST.has_key('entry_id'):
        id = int(request.POST['entry_id'])
    # otherwise use the parameter
    elif entry_id is None:
        return render_to_response('lifeflow/invalid_comment.html',{},RequestContext(request, {}))
    else:
        id = int(entry_id)
    # TODO: validate ID, throw 500 otherwise
    entry = Entry.objects.get(pk=id)
    
    if request.POST.has_key('parent_id') and request.POST['parent_id'] != u"":
        parent_id = int(request.POST['parent_id'])
        parent = Comment.objects.get(pk=parent_id)
    elif parent_id is None:
        parent = None
    else:
        parent_id = int(parent_id)
        parent = Comment.objects.get(pk=parent_id)

    # add an identifier to the post, part of the
    # anti-spam implementation
    if request.POST.has_key('identifier') is False:
        now = unicode(time.time()).split('.')[0]
        identifier = make_identifier(id, now)
    # or make a new identifier
    else:
        identifier = request.POST['identifier']
        now = request.POST['time']
        
    form = CommentForm(request.POST)
    form.is_valid()

    # Initial submission from entry_detail.html
    if request.POST.has_key('submit'):
        for i in xrange(5,8):
            name = u"honey%s" % i 
            value = request.POST[name]
            if value != u"":
                raise Http404
        if time.time() - int(now) > 3600:
            raise Http404
        if identifier != make_identifier(id, now):
            raise Http404

        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        webpage = form.cleaned_data['webpage']
        html = form.cleaned_data['html']
        body = form.cleaned_data['body']
        c = Comment(entry=entry,parent=parent,name=name,email=email,
                    webpage=webpage,body=body,html=html)
        c.save()
        url = u"%s#comment_%s" % (entry.get_absolute_url(), c.pk)
        return HttpResponseRedirect(url)

    return render_to_response(
        'lifeflow/comment.html',
        {'object':entry,'parent':parent,'identifier':identifier,'time':now,'form':form},
        RequestContext(request, {}))


def flow(request, slug):
    try:
        flow = Flow.objects.get(slug=slug)
    except Flow.DoesNotExist:
        raise Http404
    try:
        page = int(request.GET["page"])
    except:
        page = 1
    page = QuerySetPaginator(Flow.objects.get(slug=slug).latest(), 5).page(page)
    return render_to_response('lifeflow/flow_detail.html', 
                              {'object' : flow, 'page' : page,},
                              RequestContext(request, {}))


def front(request):
    try:
        page = int(request.GET["page"])
    except:
        page = 1
    page = QuerySetPaginator(Entry.current.all(), 3).page(page)
    return render_to_response('lifeflow/front.html', {'page':page}, RequestContext(request, {}))


def rss(request):
    flows = Flow.objects.all()
    return render_to_response('lifeflow/meta_rss.html', {'flows' : flows }, RequestContext(request, {}))
