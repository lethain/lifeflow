import cgi
from django import newforms as forms
from lifeflow.models import comment_markup


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
        lines = body.split("\n")
        new_lines = []
        in_code = False

        # at the moment you could disable all parsing simply by
        # having initial @@'s but no closing @@'s. Instead this
        # should only disable code escaping for code-syntax blocks
        # if there is a closing @@ as well as an opening @@
        # (admittedly, it may well crash the markdownpp if 
        # it is improperly formed... if thats any consulation)
        for line in lines:
            if line.startswith("@@") and in_code is True:
                in_code = False
            elif line.startswith("@@") and in_code is False:
                in_code = True
            if in_code is False:
                if line.startswith(">"):
                    line = ">%s" % cgi.escape(line[1:])
                else:
                    line = cgi.escape(line)
            new_lines.append(line)
        escaped = u"\n".join(new_lines)
        self.cleaned_data['rendered'] = unicode(comment_markup(escaped))
        return body
        
