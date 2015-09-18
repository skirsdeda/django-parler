"""
Custom generic managers
"""
from django.utils.importlib import import_module
from parler import appsettings


_import = (
    'TranslatableQuerySet',
    'TranslatableManager',
)
__all__ = _import + (
    'TranslationQuerySet',
    'TranslationManager',
)

# import a corresponding module from backend
_mod_name = __name__.rsplit('.', 1)[-1]
_backend_path = '{0}.{1}'.format(appsettings.PARLER_BACKEND, _mod_name)
_backend = import_module(_backend_path)

# assign all publicly visible classes to this module's scope
for cls in _import:
    vars()[cls] = getattr(_backend, cls)

# Export the names in django-hvad style too:
TranslationQueryset = vars()['TranslatableQuerySet']
TranslationManager = vars()['TranslatableManager']
