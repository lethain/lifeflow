import re
from lifeflow.markdown import markdown
import lifeflow.models

class LifeflowExtension (markdown.Extension):
    
    def __init__(self, entry):
        self.entry = entry

    def extendMarkdown(self, md, md_globals):
        preprocessor = LifeflowPreprocessor(self.entry)
        preprocessor.md = md
        md.preprocessors.insert(0, preprocessor)

    def reset(self):
        pass


def make_syntax():
    # note that the key is a tuple of the number of arguments,
    # and the name of the reference before the first space.
    # for example [refer year name] would be (2, u"refer")
    # and [absurd] would be (0, u"absurd")
    # the value is a function that accepts
    # entry, str, and then N additional parameters where
    # N is equal to the number of args specified in the
    # tuple

    # [this is my author bio][author]
    def author(entry, str):
        authors = entry.authors.all()
        if len(authors) == 1:
            return str % authors[0].get_absolute_url()
        else:
            return str % u"/author/"

    # [this is the lifeflow tag ][tag lifeflow]
    def tag(entry, str, slug):
        t = lifeflow.models.Tag.objects.get(slug=slug)
        return str % t.get_absolute_url()

    # [this is the comment with primary key 123][comment 123]
    def comment(entry, str, pk):
        c = lifeflow.models.Comment.objects.get(pk=int(pk))
        return str % c.get_absolute_url()

    # [this is the project with slug magic-wand][project magic-wand]
    def project(entry, str, slug):
        p = lifeflow.models.Project.objects.get(slug=slug)
        return str % p.get_absolute_url()


    # [remember my previous entry?][previous]
    def previous(entry, str):
        if entry.__class__.__name__ == "Entry":
            prev = entry.get_previous_article()
            if prev is None:
                return None
            return str % prev.get_absolute_url()


    # [Update: I clarified this in the next entry!][next]
    def next(entry, str):
        if entry.__class__.__name__ == "Entry":
            nxt = entry.get_next_article()
            if nxt is None:
                return None
            return str % nxt.get_absolute_url()


    # [Check out the first entry in this series][series 1]
    # [or the second entry!][series 2]
    def series_number(entry, str, nth):
        try:
            nth = int(nth)
            if nth > 0:
                nth = nth - 1
        except ValueError:
            return None
        series = entry.series.all()[0]
        if series:
            try:
                e = series.entry_set.all().order_by('pub_date')[nth]
                return str % e.get_absolute_url() 
            except IndexError:
                return None


    # [Remember the Two-Faced Django series?][series two_faced 1]
    # [Well, I wrote that too! Go me.][series jet-survival 3]
    def series_slug_number(entry, str, slug, nth):
        try:
            nth = int(nth)
            if nth > 0:
                nth = nth - 1
        except ValueError:
            return None
        try:
            series = lifeflow.models.Series.objects.get(slug=slug)
        except lifeflow.models.Series.DoesNotExist:
            return None
        try:
            e = series.entry_set.all()[nth]
            return str % e.get_absolute_url() 
        except IndexError:
            return None


    # [and check out this code!][file the_name]
    # ![ a picture that I really like][file my_pic]
    # ![ and you can abreviate it][f my_pic]
    # [this way too][f my_code]
    def file(entry, str, name):
        try:
            resource = lifeflow.models.Resource.objects.get(markdown_id=name)
            return str % resource.get_relative_url()
        except lifeflow.models.Resource.DoesNotExist:
            return None


    # [I like markdown][history md]
    # [and talk about why the lucky stiff occasionally][history why]
    # [but history is long... so...][h why]
    # [and a link to my svn][h svn_lethain]
    def history(entry, str, name):
        pass

    syntax = {}
    syntax[(0, u"previous")] = previous
    syntax[(0, u"next")] = next
    syntax[(0, u"author")] = author
    syntax[(1, u"file")] = file
    syntax[(1, u"f")] = file
    syntax[(1, u"tag")] = tag
    syntax[(1, u"comment")] = comment
    syntax[(1, u"project")] = project
    syntax[(1, u"series")] = series_number
    syntax[(2, u"series")] = series_slug_number

    return syntax



class LifeflowPreprocessor :
    
    def __init__(self, entry):
        NOBRACKET = r'[^\]\[]*'
        BRK = ( r'\[('
                + (NOBRACKET + r'(\[')*6
                + (NOBRACKET+ r'\])*')*6
                + NOBRACKET + r')\]' )
        LIFEFLOW_RE = BRK + r'\s*\[([^\]]*)\]'
        

        self.LIFEFLOW_RE = re.compile(LIFEFLOW_RE)
        self.entry = entry
        self.tags = {}
        self.syntax = make_syntax()


    def process_dynamic(self, ref):
        # if tag has already been built, ignore
        if self.tags.has_key(ref):
            return None
        parts = ref.split(u" ")
        name = parts[0]
        args = parts[1:]
        length = len(args)
        format = u"[%s]: %s" % (ref, u"%s")
        try:
            func = self.syntax[(length, name)]
            result = func(self.entry, format, *args)
            self.tags[ref] = True
            return result
        except KeyError:
            self.tags[ref] = False
            to_return = None


    def build_static_references(self):
        raw_refs = ((u'comments', u"#comments", u"Comments"),
                    (u'projects', u"/projects/", "Projects"),
                    (u'series', u"/articles/", "Series"),
                    (u'tags', u"/tags/", "Tags"))
        refs = [ u'[%s]: %s "%s"' % (x[0], x[1], x[2]) for x in raw_refs ]
        return refs


    def run (self, lines):
        def clean(match):
            return match[-1]
        text = u"\n".join(lines)
        refs = self.LIFEFLOW_RE.findall(text)
        
        cleaned = [ clean(x) for x in refs ]
        processed = [ self.process_dynamic(x) for x in cleaned]
        dynamic_refs = [ x for x in processed if x is not None ]
        static_refs = self.build_static_references()
        return static_refs + dynamic_refs + lines



def makeExtension(configs=None) :
    return LifeflowExtension(configs)
    
