"""
The models and fields for translation support.

The default is to use the :class:`TranslatedFields` class in the model, like:

.. code-block:: python

    from django.db import models
    from parler.models import TranslatableModel, TranslatedFields


    class MyModel(TranslatableModel):
        translations = TranslatedFields(
            title = models.CharField(_("Title"), max_length=200)
        )

        class Meta:
            verbose_name = _("MyModel")

        def __unicode__(self):
            return self.title


It's also possible to create the translated fields model manually:

.. code-block:: python

    from django.db import models
    from parler.models import TranslatableModel, TranslatedFieldsModel
    from parler.fields import TranslatedField


    class MyModel(TranslatableModel):
        title = TranslatedField()  # Optional, explicitly mention the field

        class Meta:
            verbose_name = _("MyModel")

        def __unicode__(self):
            return self.title


    class MyModelTranslation(TranslatedFieldsModel):
        master = models.ForeignKey(MyModel, related_name='translations', null=True)
        title = models.CharField(_("Title"), max_length=200)

        class Meta:
            verbose_name = _("MyModel translation")

This has the same effect, but also allows to to override
the :func:`~django.db.models.Model.save` method, or add new methods yourself.

The translated model is compatible with django-hvad, making the transition between both projects relatively easy.
The manager and queryset objects of django-parler can work together with django-mptt and django-polymorphic.
"""
from django.utils.importlib import import_module
from parler import appsettings
from parler.bases.models import TranslationDoesNotExist  # noqa


_import = (
    'TranslatableModel',
    'TranslatedFields',
    'TranslatedFieldsModel',
    'TranslatedFieldsModelBase',
)
__all__ = _import + (
    'TranslationDoesNotExist',
)

# import a corresponding module from backend
_mod_name = __name__.rsplit('.', 1)[-1]
_backend_path = '{0}.{1}'.format(appsettings.PARLER_BACKEND, _mod_name)
_backend = import_module(_backend_path)

# assign all publicly visible classes to this module's scope
for cls in _import:
    vars()[cls] = getattr(_backend, cls)
