from django.template import RequestContext
from django.shortcuts import render_to_response

def server_error(request):
    return render_to_response('500.html',{},RequestContext(request,{}))
