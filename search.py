import solango
from lifeflow.models import Comment, Entry

class EntryDocument(solango.SearchDocument):
    date = solango.fields.DateField()
    title = solango.fields.CharField(copy=True)
    content = solango.fields.TextField(copy=True)
    
    def transform_date(self, instance):
        return instance.pub_date

    def transform_content(self, instance):
        return instance.body

solango.register(Entry, EntryDocument)
