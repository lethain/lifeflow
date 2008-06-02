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
from lifeflow.models import Series, Flow, Entry, Comment
from lifeflow.forms import CommentForm


def articles(request):
    def comp(a,b):
        result = b.num_articles() - a.num_articles()
        return int(result)
        
    object_list = Series.objects.all()._get_data()
    object_list.sort(comp)
    return render_to_response(
        'lifeflow/articles.html',
        {'object_list' : object_list},
        RequestContext(request, {}),
        )


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
        rendered = form.cleaned_data['rendered']
        body = form.cleaned_data['body']
        c = Comment(entry=entry,
                    parent=parent,
                    name=name,
                    email=email,
                    webpage=webpage,
                    body=body,
                    html=rendered,
                    )
        c.save()
        url = u"%s#comment_%s" % (entry.get_absolute_url(), c.pk)
        return HttpResponseRedirect(url)

    return render_to_response(
        'lifeflow/comment.html',
        {'object': entry,
         'parent': parent,
         'identifier' : identifier,
         'time' : now,
         'form': form,
         },
        RequestContext(request, {}),
        )



def flow(request, slug):
    num_per_page = 10
    try:
        first = request.GET["end_at"]
        first = int(first)
        last = first + num_per_page
    except KeyError:
        first = 0
        last = num_per_page
    flow = Flow.objects.get(slug=slug)
    object_list = flow.latest()[first:last]
    count = flow.entry_set.all().count()
    if last >= count:
        at_end = True
    else:
        at_end = False
    if first > 0:
        at_start = False
        previous = first - num_per_page
    else:
        at_start = True
        previous = None

    return render_to_response(
        'lifeflow/flow_detail.html',
        {
            'object' : flow,
            'object_list' : object_list,
            'last' : last,
            'previous' : previous,
            'at_start' : at_start,
            'at_end' : at_end,
         },
        RequestContext(request, {}),
        )


def front(request):
    comments = Comment.objects.all().order_by('-date')[:5]
    return render_to_response(
        'lifeflow/front.html',
        {'comments':comments,},
        RequestContext(request, {}),
        )



def rss(request):
    flows = Flow.objects.all()
    return render_to_response(
        'lifeflow/meta_rss.html',
        {'flows' : flows },
        RequestContext(request, {}),
        )
