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


CODE_BLOCK_REGEX = re.compile(r"@@ (?P<syntax>[a-zA-Z0-9_+-]+)\r?\n(?P<code>.*?)@@\r?\n", re.DOTALL)

class CodeBlockPreprocessor :
    def run (self, text):
        while  1:
            m = CODE_BLOCK_REGEX.search(text)
            if not m: break;
            lexer = get_lexer_by_name(m.group('syntax'))
            color = highlight(m.group('code'), lexer, HtmlFormatter())
            placeholder = self.md.htmlStash.store(color, safe=True)
            text = '%s\n%s\n%s'% (text[:m.start()], placeholder, text[m.end():])
        return text


def makeExtension(configs=None) :
    return CodeExtension(configs=configs)

