
import os
import logging

from Cheetah.Template import Template

try:
    from hashlib import sha1
except ImportError:
    import sha
    def sha1(str):
        return sha.new(str)

here = os.path.dirname(__file__)

class GoCaptain(object):

    """ Use this class from other buildout recipes - it is easier to call than
    the buildout recipe itself. """

    template = None
    template_str = None
    defaults = {}
    required = []

    def __init__(self, template=None, template_str=None, defaults={}, required=[]):
        self.template = template
        self.template_str = template_str
        self.defaults = defaults
        self.required = required

    def write(self, stream, **kw):
        for i in self.notsupported:
            if i in kw:
                raise KeyError("Unsupported option: %s" % i)
        for i in self.required:
            if not i in kw:
                raise KeyError("Missing option: %s" % i)
        for k, v in self.defaults.items():
            kw.setdefault(k, v)
        if self.template is not None:
            t = open(self.template).read()
        else:
            t = self.template_str
        c = Template(t, searchList=kw)
        stream.write(str(c))

class Simple(GoCaptain):
    template = os.path.join(here, "simple.tmpl")
    defaults = {
            'preamble': '',
        }
    required =  [
            'daemon',
            'description',
            'pidfile',
            'args',
        ]
    notsupported = [
            'background',
    ]

    def __init__(self):
        pass

class LinuxStandardBase(GoCaptain):
    template = os.path.join(here, "lsb.tmpl")
    defaults = {
            'preamble': '',
        }
    required = [
            'name',
            'description',
            'daemon',
            'pidfile',
            'args',
        ]
    notsupported = [
    ]

    def __init__(self):
        pass

class Automatic(object):

    def __init__(self, *a, **kw):
        if os.path.exists('/lib/lsb/init-functions'):
            self.__class__ = LinuxStandardBase
        else:
            self.__class__ = Simple


class Buildout(GoCaptain):

    """ This is the base class for the buildout recipes below """

    def __init__(self, buildout, name, options):
        self.name = name
        self.options = options
        self.buildout = buildout
        self.logger = logging.getLogger(self.name)
        if self.template is not None:
            self.options.setdefault("template", self.template)

            # Record a SHA1 of the template we use, so we can detect changes in subsequent runs
            self.options["__hashes_template"] = sha1(open(self.options["template"]).read()).hexdigest()

    def install(self):
        if 'template' in self.options:
            self.template = self.options['template']
        target = os.path.join(self.buildout['buildout']['bin-directory'], self.name)
        try:
            self.write(open(target, "w"), **self.options.copy())
        except KeyError:
            os.unlink(target)
            raise
        os.chmod(target, 0755)
        self.options.created(target)
        return self.options.created()

    def update(self):
        pass

class SimpleBuildout(Buildout, Simple):
    pass

class LinuxStandardBaseBuildout(LinuxStandardBase, Buildout):
    pass

class AutomaticBuildout(object):

    def __init__(self, *a, **kw):
        if os.path.exists('/lib/lsb/init-functions'):
            self.__class__ = LinuxStandardBaseBuildout
        else:
            self.__class__ = SimpleBuildout
        Buildout.__init__(self, *a, **kw)
