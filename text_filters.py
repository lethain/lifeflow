"""
    This file contains filters which are used for pre and post
    processing various kinds of text within LifeFlow.

    Which values are applied is controlled by a number of global
    variables within the project's settings.py file. These vars
    are:

    LIFEFLOW_ENTRY_FILTERS
    LIFEFLOW_COMMENT_FILTERS

    If you wish to add your own filters, you don't
    have to add them to this file, they can exist anywhere, and
    simply import them into the settings.py file and add them
    to the appropriate global variable.

    The API for these processing functions is very simple:
    they accept two parameters, a string to process,
    and optionally a related model.
"""

from django.conf import settings
from lifeflow.markdown.markdown import Markdown
from lifeflow.markdown import mdx_lifeflow
from lifeflow.markdown import mdx_code
from lifeflow.markdown import mdx_footnotes
from lifeflow.markdown import mdx_foreign_formats



def comment_markup(txt,obj=None):
    filters = getattr(settings,'LIFEFLOW_COMMENT_FILTERS', DEFAULT_COMMENT_FILTERS)
    for filter in filters:
        txt = filter(txt)
    return txt

def entry_markup(txt,obj=None):
    filters = getattr(settings,'LIFEFLOW_ENTRY_FILTERS', DEFAULT_ENTRY_FILTERS)
    for filter in filters:
        txt = filter(txt)
    return txt


def comment_markdown(txt,obj=None):
    exts = (mdx_code,)
    md = Markdown(txt,extensions=exts,safe_mode=True)
    return md.convert()


def entry_markdown(txt,obj=None):
    exts = (mdx_code, mdx_footnotes,mdx_foreign_formats, mdx_lifeflow)
    md = Markdown(txt,extensions=exts,extension_configs={'lifeflow':obj})
    return md.convert()
    

DEFAULT_COMMENT_FILTERS = (comment_markdown,)
DEFAULT_ENTRY_FILTERS = (entry_markdown,)
