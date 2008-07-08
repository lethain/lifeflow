import re
from lifeflow.markdown import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


class CodeExtension (markdown.Extension):

    def __name__(self):
        return u"code"

    def extendMarkdown(self, md, md_global):
        preprocessor = CodeBlockPreprocessor()
        preprocessor.md = md
        md.textPreprocessors.insert(0, preprocessor)


CODE_BLOCK_REGEX = re.compile(r"\r?\n(?P<spaces>[ ]*)@@[ ]*(?P<syntax>[a-zA-Z0-9_+-]+)[ ]*(?P<linenos>[a-zA-Z]*)[ ]*\r?\n(?P<code>.*?)@@[ ]*\r?\n", re.DOTALL | re.MULTILINE)

class CodeBlockPreprocessor :
    def run (self, text):
        print "searching for matches"
        print text
        print len(text)
        while  1:
            m = CODE_BLOCK_REGEX.search(text)
            if not m: break;
            print m
            spaces = len(m.group('spaces'))
            lexer = get_lexer_by_name(m.group('syntax'))
            linenos = m.group('linenos')
            unspaced = [x[spaces:] for x in re.split('\r?\n', m.group('code'))]
            color = highlight("\n".join(unspaced), lexer, HtmlFormatter(linenos=linenos))
            placeholder = self.md.htmlStash.store(color, safe=True)
            text = '%s\n%s\n%s'% (text[:m.start()], (' '*spaces)+placeholder, text[m.end():])
        return text


def makeExtension(configs=None) :
    return CodeExtension(configs=configs)

