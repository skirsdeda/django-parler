from django.core.exceptions import ObjectDoesNotExist

class TranslationDoesNotExist(AttributeError, ObjectDoesNotExist):
    """
    A tagging interface to detect missing translations.
    The exception inherits from :class:`~exceptions.AttributeError` to reflect what is actually happening.
    Therefore it also causes the templates to handle the missing attributes silently, which is very useful in the admin for example.
    The exception also inherits from :class:`~django.core.exceptions.ObjectDoesNotExist`,
    so any code that checks for this can deal with missing translations out of the box.

    This class is also used in the ``DoesNotExist`` object on the translated model, which inherits from:

    * this class
    * the ``sharedmodel.DoesNotExist`` class
    * the original ``translatedmodel.DoesNotExist`` class.

    This makes sure that the regular code flow is decently handled by existing exception handlers.
    """
    pass


class TranslatedFieldsBase(object):
    """
    Wrapper class to define translated fields on a model.

    The field name becomes the related name of the :class:`TranslatedFieldsModel` subclass.

    Example:

    .. code-block:: python

        from django.db import models
        from parler.models import TranslatableModel, TranslatedFields

        class MyModel(TranslatableModel):
            translations = TranslatedFields(
                title = models.CharField("Title", max_length=200)
            )

    When the class is initialized, the attribute will point
    to a :class:`~django.db.models.fields.related.ForeignRelatedObjectsDescriptor` object.
    Hence, accessing ``MyModel.translations.related.model`` returns the original model
    via the :class:`django.db.models.related.RelatedObject` class.

    ..
       To fetch the attribute, you can also query the Parler metadata:
       MyModel._parler_meta.get_model_by_related_name('translations')
    """
    def __init__(self, meta=None, **fields):
        self.fields = fields
        self.meta = meta
        self.name = None

    def contribute_to_class(self, cls, name):
        # Called from django.db.models.base.ModelBase.__new__
        self.name = name
