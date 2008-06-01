from django.contrib.sitemaps import Sitemap
from lifeflow.models import Project, Entry

class ProjectSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.9
    
    def items(self):
        return Project.objects.all()
