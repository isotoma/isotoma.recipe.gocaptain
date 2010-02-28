import unittest
from StringIO import StringIO
import tempfile
import os
import UserDict

from isotoma.recipe.gocaptain import GoCaptain, Buildout

class MockOptions(UserDict.IterableUserDict):
    def __init__(self, *a, **kw):
        UserDict.IterableUserDict.__init__(self, *a, **kw)
        self._created = []
    def created(self, *p):
        self._created.extend(p)

class TestGoCaptain(unittest.TestCase):

    def test_basic(self):
        t = "$foo"
        g = GoCaptain(template_str=t)
        o = StringIO()
        g.write(o, foo="bar")
        self.assertEqual(o.getvalue(), "bar")

    def test_defaults(self):
        t = "$foo"
        g = GoCaptain(template_str=t, defaults={'foo': 'bar'})
        o = StringIO()
        g.write(o)
        self.assertEqual(o.getvalue(), "bar")

    def test_required(self):
        t = "$foo"
        g = GoCaptain(template_str=t, required=['foo'])
        o = StringIO()
        self.assertRaises(KeyError, g.write, o)

class X(Buildout):
    template = os.path.join(os.path.dirname(__file__), "basic.tmpl")
    defaults = {'foo': 'bar'}
    required = ['baz']

class TestBuildout(unittest.TestCase):

    def setUp(self):
        self.td = tempfile.mkdtemp()
        self.buildout = {
            'buildout': {
                'bin-directory': self.td,
            }
        }

    def test_basic(self):
        options = MockOptions({'foo': 'quux', 'baz': 'quuux'})
        x = X(self.buildout, "name", options)
        x.install()
        target = os.path.join(self.td, 'name')
        self.assertEqual(options._created, [target])
        d = open(target).read()
        self.assertEqual(d, "quux")
        os.unlink(target)
        os.rmdir(self.td)

    def test_defaults(self):
        options = MockOptions({'baz': 'quuux'})
        x = X(self.buildout, "name", options)
        x.install()
        target = os.path.join(self.td, 'name')
        self.assertEqual(options._created, [target])
        d = open(target).read()
        self.assertEqual(d, "bar")
        os.unlink(target)
        os.rmdir(self.td)

    def test_required(self):
        options = MockOptions()
        x = X(self.buildout, "name", options)
        self.assertRaises(KeyError, x.install)
        os.rmdir(self.td)



