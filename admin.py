from django.contrib import admin
from lifeflow.models import *


class CommentAdmin(admin.ModelAdmin):
    list_display = ('entry', 'name', 'email', 'webpage', 'date')
    search_fields = ['name', 'email','body']
    
admin.site.register(Comment, CommentAdmin)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'link')
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
admin.site.register(Author, AuthorAdmin)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    search_fields = ['title', 'summary', 'body']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('flows','tags','series','resources','authors')
    fieldsets = (
        (None, {'fields' : ('title', 'slug', 'pub_date',)}),
        ('Content', {'fields': ('summary', 'body',)}),
        ('Options', {'fields': ('use_markdown', 'is_translation', 'send_ping', 'allow_comments', ), 'classes': 'collapse'}),
        ('Authors', {'fields' : ('authors',), 'classes': 'collapse'}),
        ('Resources', {'fields' : ('resources',), 'classes': 'collapse'}),
        ('Series', {'fields': ('series',), 'classes': 'collapse'}),
        ('Organization', {'fields': ('flows', 'tags',),}),
        )
        
admin.site.register(Entry, EntryAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'license', 'size',)
    search_fields = ['title', 'summary', 'body']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('resources',)
    fieldsets = (
        (None, {'fields' : ('title', 'slug', 'size', 'language', 'license', 'use_markdown',)} ),
        ('Content', {'fields': ('summary', 'body', 'resources')} ),
        )

admin.site.register(Project, ProjectAdmin)

# Custom admins required due to slug field
class SeriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Series, SeriesAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Tag, TagAdmin)

class FlowAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)} 
admin.site.register(Flow, FlowAdmin)

class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Language, LanguageAdmin)

# Simple admin interfaces
admin.site.register(Resource)
admin.site.register(RecommendedSite)
admin.site.register(SiteToNotify)
admin.site.register(Translation)