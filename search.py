import solango
from lifeflow.models import Comment, Entry

class EntryDocument(solango.SearchDocument):
    date = solango.fields.DateField()
    summary = solango.fields.TextField(copy=True)
    title = solango.fields.CharField(copy=True)
    tags = solango.fields.CharField(copy=True)
    content = solango.fields.TextField(copy=True)

    def transform_summary(self, instance):
        return instance.summary

    def transform_tags(self, instance):
        tags = list(instance.tags.all())
        texts = [ tag.title for tag in tags ]
        return ",".join(texts)
    
    def transform_date(self, instance):
        return instance.pub_date

    def transform_content(self, instance):
        return instance.body

solango.register(Entry, EntryDocument)
