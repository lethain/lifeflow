import re
from lifeflow.markdown import markdown
from django.utils.encoding import smart_str, force_unicode

class ForeignFormatsExtension (markdown.Extension):

    def __name__(self):
        return u"foreign formats"

    def extendMarkdown(self, md, md_global):
        preprocessor = ForeignFormatsBlockPreprocessor()
        preprocessor.md = md
        md.textPreprocessors.insert(0, preprocessor)


FORMATTERS = {}

# Attempt to import textile formatter.
try:
    # http://dealmeida.net/projects/textile/
    import textile
    def func(x):
        return textile.textile(smart_str(x), encoding='utf-8', output='utf-8')

    FORMATTERS["textile"] = func
except ImportError:
    pass

# Attempt to import docutiles (ReST) formatter.
try:
    # http://docutils.sf.net/
    from docutils.core import publish_parts
    def func(x):
        return publish_parts(source=x,writer_name="html4css1")["fragment"]

    FORMATTERS["rest"] = func
except ImportError:
    pass


FOREIGN_FORMAT_BLOCK_REGEX = re.compile(r"^~~~(?P<format>\w*)\r?\n(?P<txt>.*?)^~~~$", re.DOTALL|re.MULTILINE)


class ForeignFormatsBlockPreprocessor :
    def run (self, text):
        while  1:
            m = FOREIGN_FORMAT_BLOCK_REGEX.search(text)
            if not m: break;
            format = m.group('format').lower()
            txt = m.group('txt')
            if FORMATTERS.has_key(format):
                func = FORMATTERS[format]
                txt = func(txt)
            placeholder = self.md.htmlStash.store(txt, safe=True)
            text = '%s\n%s\n%s'% (text[:m.start()], placeholder, text[m.end():])
        return text


def makeExtension(configs=None) :
    return ForeignFormatsExtension(configs=configs)

