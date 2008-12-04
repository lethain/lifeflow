from django.db import models

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
