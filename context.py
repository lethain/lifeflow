from lifeflow.models import Entry, Flow, RecommendedSite, Author, Flow, Language
from django.contrib.sites.models import Site
from django.conf import settings


def blog(request):
    def make_slug(str):
        return str.lower().replace(" ","-")
    recent = Entry.current.all()[:5]
    random = Entry.current.all().order_by('?')[:5]
    blog_roll = RecommendedSite.objects.all()
    flows = Flow.objects.all()
    site = Site.objects.get(pk=settings.SITE_ID)
    analytics_id = getattr(settings, 'LIFEFLOW_GOOGLE_ANALYTICS_ID', None)
    use_projects = getattr(settings, 'LIFEFLOW_USE_PROJECTS', True)
    keywords = getattr(settings, 'LIFEFLOW_KEYWORDS', "blog")
    description = getattr(settings, 'LIFEFLOW_DESCRIPTION', "blog")
    author = getattr(settings, 'LIFEFLOW_AUTHOR_NAME', None)
    template_author = getattr(settings, 'LIFEFLOW_TEMPLATE_AUTHOR', "Will Larson")
    template_author_url = getattr(settings, 'LIFEFLOW_TEMPLATE_AUTHOR_URL', "http://www.lethain.com/")
    if author is None:
        try:
            author = Author.objects.get(pk=1).name
        except:
            author = "Anonymous"

    author_slug = make_slug(author)
    blog_name = getattr(settings, 'LIFEFLOW_BLOG_NAME', "Unconfigured LifeFlow")
    custom_css = getattr(settings, 'LIFEFLOW_CUSTOM_CSS', None)
    custom_js_header = getattr(settings, 'LIFEFLOW_CUSTOM_JS_HEADER', None)
    custom_js_footer = getattr(settings, 'LIFEFLOW_CUSTOM_JS_FOOTER', None)
    return {
        'blog_roll' : blog_roll,
        'lifeflow_google_analytics_id':analytics_id,
        'lifeflow_blog_name':blog_name,
        'lifeflow_custom_css':custom_css,
        'lifeflow_custom_js_header':custom_js_header,
        'lifeflow_custom_js_footer':custom_js_footer,
        'lifeflow_flows':flows,
        'lifeflow_keywords':keywords,
        'lifeflow_description':description,
        'lifeflow_author':author,
        'lifeflow_author_slug':author_slug,
        'lifeflow_use_projects':use_projects,
        'lifeflow_template_author':template_author,
        'lifeflow_template_author_url':template_author_url,
        'recent_entries' : recent, 
        'random_entries' : random,
        'site' : site,
        }
