import cgi
from django import newforms as forms
from lifeflow.text_filters import comment_markup


class CommentForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    webpage = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea, required=False)


    def clean_name(self):
        name = self.cleaned_data['name']
        if name == u"":
            name = u"name"
        else:
            name = cgi.escape(name)
        return name
        

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == u"":
            email = u"email"
        else:
            email = cgi.escape(email)
        return email


    def clean_webpage(self):
        webpage = self.cleaned_data['webpage']
        if webpage == u"":
            webpage = u"webpage"
        else:
            webpage = cgi.escape(webpage)
        if webpage.find('://') == -1: webpage = "http://%s" % webpage
        return webpage
        

    def clean_body(self):
        body = self.cleaned_data['body']
        self.cleaned_data['html'] = unicode(comment_markup(body))
        return body
        
