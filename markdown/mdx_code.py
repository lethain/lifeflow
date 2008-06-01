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


class CodeBlockPreprocessor :

    def run (self, text):
        text.replace("\r\n","\n")
        lines = text.split("\n")
        new_lines = []
        seen_start = False
        lang = None
        block = []
        for line in lines:
            if line.startswith("@@") is True and seen_start is False:
                lang = line.strip("@@ ")
                seen_start = True
            elif line.startswith("@@") is True and seen_start is True:
                content = u"\n".join(block)
                try:
                    lexer = get_lexer_by_name(lang)
                    highlighted = highlight(content, lexer, HtmlFormatter())
                    new_lines.append(u"%s" % (highlighted))
                except:
                    new_lines.append(u"<pre>%s</pre>" % content)
                lang = None
                block = []
                seen_start = False
            elif seen_start is True:
                block.append(line)
            else:
                new_lines.append(line)
        return u"\n".join(new_lines)


def makeExtension(configs=None) :
    return CodeExtension(configs=configs)

