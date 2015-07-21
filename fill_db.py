import pkgutil
import django
import re
import importlib
import inspect
from django.contrib.admin.sites import AlreadyRegistered
from django.core.exceptions import ImproperlyConfigured
from search.models import Name

p = ur'import( [^\d\W]\w*,?)* %s'
wow = []
failed = []
all_names = []
all_names_objs = []
modules = []
for loader, module_name, is_pkg in pkgutil.walk_packages(django.__path__):
    wow.append(module_name)
    module = None
    try:
        module = loader.find_module(module_name).load_module(module_name)
        modules.append((module_name, module))
    except (RuntimeError, AlreadyRegistered, ImproperlyConfigured, ImportError,
            NameError, TypeError) as e:
        try:
            module = importlib.import_module('django.' + module_name)
            modules.append((module_name, module))
        except (ImproperlyConfigured, ImportError, NameError):
            failed.append(module_name)
    if module:
        if hasattr(module, '__all__'):
            for name in module.__all__:
                pass
                # Name.objects.update_or_create(name=name, module_name=module_name,
                #                               defaults={'is_from_all': True})


# second run

for module_name, module in modules:
    for i in inspect.getmembers(module, lambda x: not inspect.ismodule(x)):
        if not i[0].startswith('_'):
            all_names.append('django.' + module_name + '.' + i[0])
            if not Name.objects.filter(name=i[0], is_from_all=True).exists():
                if not re.search(p % i[0], inspect.getsource(module)):
                    all_names_objs.append(Name(name=i[0], module_name=module_name))
Name.objects.filter(is_from_all=False).delete()
Name.objects.bulk_create(all_names_objs)
