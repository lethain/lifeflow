"""
Import any enabled modules as specified in the settings.py
file for the project.

"""

import imp
import sys
from django.conf import settings


def import_module(name, globals=None, locals=None, fromlist=None):
    # Fast path: see if the module has already been imported.
    try:
        return sys.modules[name]
    except KeyError:
        pass

    # If any of the following calls raises an exception,
    # there's a problem we can't handle -- let the caller handle it.

    _, pathname, description = imp.find_module("lifeflow")
    path = u"%s/mods/%s" % (pathname, name)
    return imp.load_module(name, None, path, description)


for mod in getattr(settings, u"LIFEFLOW_MODS", ()):
    import_module(mod)

