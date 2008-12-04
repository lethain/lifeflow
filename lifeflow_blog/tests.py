import unittest
from django.test.client import Client
from lifeflow.models import *
import datetime
import pygments.lexers as lexers



#response = self.client.get('/api/case/retrieve/', {})
#self.assertEquals(response.content, 'etc')

class commentTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_organize_comments(self):
        "models.py: test organize_comments method for Entry"
        e = Entry(title="My Entry",
                  pub_date=datetime.datetime.now(),
                  summary="A summary",
                  body="Some text")
        e.save()
        c1 = Comment(entry=e, body="Some comment one.")
        c1.save()
        self.assertEquals([[c1, 0]], e.organize_comments())
        c2 = Comment(entry=e, name="Two", body="Some comment two.")
        c2.save()
        self.assertEquals([[c2,0],[c1,0]], e.organize_comments())
        c3 = Comment(entry=e, name="Three", parent=c1, body="Three")
        c3.save()
        self.assertEquals([[c2, 0], [c1,0], [c3,1]],
                          e.organize_comments())
        c4 = Comment(entry=e, name="Four", parent=c2, body="Four")
        c4.save()
        self.assertEquals([[c2,0], [c4, 1], [c1,0], [c3,1]],
                          e.organize_comments())


class codeMarkupTest(unittest.TestCase):
    def test_markup(self):
        "markup/markdown.py: test markdown"
        txt = "this is some text"
        expected = u"<p>this is some text\n</p>"
        rendered = dbc_markup(txt).strip("\n")
        self.assertEqual(expected, rendered)
        
    def test_code_markup(self):
        "markup/code.py: test code markup"

        txt = u"    some code in a code block\n    is nice\n"
        expected = u'<pre><code>some code in a code block\nis nice\n</code></pre>'
        self.assertEqual(expected, dbc_markup(txt))

        txt = u"<pre>this is some stuff\nthat I am concerned about</pre>"
        self.assertEqual(txt, dbc_markup(txt))

        txt = u"@@ python\nx = 10 * 5\n@@\n"
        expected = u'<div class="highlight"><pre><span class="n">x</span> <span class="o">=</span> <span class="mi">10</span> <span class="o">*</span> <span class="mi">5</span>\n</pre></div>'
        self.assertEqual(expected, dbc_markup(txt))


        txt = u"@@ python\ndef test(a,b):\n    return x + y\n@@\n"
        expected = u'<div class="highlight"><pre><span class="k">def</span> <span class="nf">test</span><span class="p">(</span><span class="n">a</span><span class="p">,</span><span class="n">b</span><span class="p">):</span>\n    <span class="k">return</span> <span class="n">x</span> <span class="o">+</span> <span class="n">y</span>\n</pre></div>'
        self.assertEqual(expected, dbc_markup(txt))

        


    def test_using_non_existant_language(self):
        "markup/code.py: test improperly formed code markup"
        cases = (
            u"@@\ndef test(a,b):\n@@\n",
            u"@@ fake-language\n(+ 1 2 3)\n@@\n",
            )
        for case in cases:     
            self.assertRaises(lexers.ClassNotFound, 
                              lambda : dbc_markup(case))
         

    def test_lfmu(self):
        "markup/lifeflowmarkdown.py: test lifeflow markup"
        e = Entry(title="My Entry",
                  pub_date=datetime.datetime.now(),
                  summary="A summary",
                  body="Some text")
        e.save()

        a = Author(name="Will Larson",
                   slug="will-larson",
                   link="a")
        a.save()

        e2= Entry(title="My Entry",
                  pub_date=datetime.datetime.now(),
                  summary="A summary",
                  body="Some text",
                  )
        e2.save()
        e2.authors.add(a)
        e2.save()

        t = Tag(title="LifeFlow", slug="lifeflow")
        t.save()

        c1 = Comment(entry=e, body="Some comment one.")
        c1.save()

        p = Project(title="Lifeflow",
                    slug="lifeflow",
                  summary="A summary",
                  body="Some text")
        p.save()

        
        self.assertEqual(dbc_markup("[trying out a tag][tag lifeflow]", e),
                         u'<p><a href="/tags/lifeflow/">trying out a tag</a>\n</p>')
        self.assertEqual(dbc_markup("[and the author][author]", e),
                         u'<p><a href="/author/">and the author</a>\n</p>')
        self.assertEqual(dbc_markup("[about will][author]", e2),
                      u'<p><a href="/author/will-larson/">about will</a>\n</p>')
        #self.assertEqual(dbc_markup("[the first comment][comment 1]", e),
        #                 u'<p><a href="/entry/2008/jan/12//#comment_1">the first comment</a>\n</p>')
        self.assertEqual(dbc_markup("[lf proj][project lifeflow]", e),
                         u'<p><a href="/projects/lifeflow/">lf proj</a>\n</p>')

        # test for [file name]
        # test for [f name]
