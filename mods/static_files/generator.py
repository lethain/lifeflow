"""Static file generator for Django."""

__version__ = 'pre0.97, 2008-1-11'

#
# Some updating for working with current django SVN. pre0.97
#
#

# The MIT License
# 
# Copyright(c) 2008 Will Larson 
# (although full credit is due to Jared Kuolt, I'm not certain what the
#  etiquete should be here, because he wrote most everything, but I have
#  slightly updated it...)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
from django.http import HttpRequest
from django.core.handlers.base import BaseHandler
from django.db.models.base import ModelBase
from django.db.models.manager import Manager
from django.db.models import Model
from django.db.models.query import QuerySet
from django.conf import settings
from django.utils.functional import Promise

class DummyHandler(BaseHandler):
    """Required to process request and response middleware"""
    
    def __call__(self, request):
        self.load_middleware()
        response = self.get_response(request)
        for middleware_method in self._response_middleware:
            response = middleware_method(request, response)
            
        return response    

class StaticGeneratorException(Exception):
    pass

class StaticGenerator(object):
    """
    The StaticGenerator class is created for Django applications, like a blog,
    that are not updated per request.
    
    Usage is simple::
    
        from blog.models import Post
        from django.contrib.flatpages.models import FlatPage
        gen = StaticGenerator(['/', Post.objects.live(), FlatPage])
        gen.publish()
        
    The class accepts a list of 'resources' which can be any of the 
    following: URL path (string), Model (class or instance), Manager, or 
    QuerySet.
    
    The most effective usage is to associate a StaticGenerator with a model's
    pre_ or post_save signal.
    
    """
    
    def __init__(self, resources):
        self.resources = self.extract_resources(resources)
        try:
            self.web_root = getattr(settings, 'WEB_ROOT')
        except AttributeError:
            raise StaticGeneratorException('You must specify WEB_ROOT in settings.py')
        
    def extract_resources(self, resources):
        """Takes a list of resources, and gets paths by type"""
        extracted = []
        for resource in resources:
            
            # A URL string
            if isinstance(resource, (str, unicode, Promise)):
                extracted.append(str(resource))
                continue
            
            # A model instance; requires get_absolute_url method
            if isinstance(resource, Model):
                extracted.append(resource.get_absolute_url())
                continue
            
            # If it's a Model, we get the base Manager
            if isinstance(resource, ModelBase):
                resource = resource._default_manager
            
            # If it's a Manager, we get the QuerySet
            if isinstance(resource, Manager):
                resource = resource.all()
            
            # Append all paths from obj.get_absolute_url() to list
            if isinstance(resource, QuerySet):
                for obj in resource:
                    extracted.append(obj.get_absolute_url())
        
        return extracted
    
    def get_content_from_path(self, path):
        """
        Imitates a basic http request using DummyHandler to retrieve
        resulting output (HTML, XML, whatever)
        
        """
        request = HttpRequest()
        request.path = path
        request.META[u"SERVER_NAME"] = "localhost"
        request.META[u"SERVER_PORT"] = 80
        
        handler = DummyHandler()
        response = handler(request)
        
        return response.content
        
    def get_filename_from_path(self, path):
        """Creates index.html for path or just returns path as filename"""
        if path.endswith('/'):
            path = '%sindex.html' % path
        
        return os.path.join(self.web_root, path[1:])
        
    def publish_from_path(self, path):
        """
        Gets filename and content for a path, attempts to create directory if 
        necessary, writes to file.
        
        """
        fn = self.get_filename_from_path(path)
        content = self.get_content_from_path(path)
        directory = os.path.dirname(fn)
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except:
                raise StaticGeneratorException('Could not create the directory: %s' % directory)
        
        try:
            f = open(fn, 'w')
            f.write(content)
            f.close()
        except:
            raise StaticGeneratorException('Could not create the file: %s' % fn)
    
    def publish(self):
        """Publishes all resources"""
        for path in self.resources:
            self.publish_from_path(path)

def quick_publish(resources):
    gen = StaticGenerator(resources)
    gen.publish()
