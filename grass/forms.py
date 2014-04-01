from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models.query import QuerySet

from .exceptions import WrongModelError
from .utils import get_foreign_key


class BaseNode(object):

    model = None
    fields = ()

    def autocomplete(self, query):
        raise NotImplementedError

    def choice_fields(self, instance):
        # TODO Un po' brutto. Sarebbe bello un iteratore
        return [i(instance) for i in self.fields]


class MultipleChoiceFieldFactory(object):
    """
    Callable class that helps building or customize the queryset to be passed
    to a django.forms.ModelMultipleChoiceField class or subclass, starting from
    an instance of a model that has a foreign key to the model of the queryset
    or is part of a chain or related models.
    
    It accepts the following parameters:
    - model_class: the model class to build the queryset upon
    - instance_lookup: in case of multiple foreign keys from the instance model
                       to the queryset model, it's possible to specify which one
                       to use directly through the complete lookup, otherwise
                       the class will look automatically for the right lookup.
                       Can even be used when the model of the instance has to
                       hop through another model to get to model_class
    - filter_lookup: an extra dictionary to further filter queryset objects
    - exclude_lookup: an extra dictionary to further exclude queryset objects
    - queryset: this is the last resort to completely override the construction
                of the queryset. The only requirements is that the model of the
                queryset is the same of the model_class parameter, otherwise a
                WrongModelError is raised
    - field_class: the class of the field to build. By default it is a
                   django.forms.ModelMultipleChoiceField class, but can be any
                   class as long as it accepts a queryset parameter
    
    By default, the queryset attached to the field is a simple foreign key
    lookup filter.
    """
    def __init__(self, model_class, instance_lookup=None, filter_lookup=None,
        exclude_lookup=None, queryset=None, field_class=forms.ModelMultipleChoiceField):
        # TODO Decidere se passare una classe per il field oppure una per il widget
        self.model_class = model_class
        self.instance_lookup = instance_lookup
        self.filter_lookup = filter_lookup or {}
        self.exclude_lookup = exclude_lookup or {}
        self.queryset = queryset
        self.field_class = field_class

    def __call__(self, instance):
        content_type = ContentType.objects.get_for_model(self.model_class)
        queryset = self.get_queryset(instance)
        field = self.field_class(queryset=queryset)
        field.widget.attrs.update({'data-grass-ct': content_type.pk})
        return field

    def _get_fk_name(self, instance):
        opts = instance._meta
        parent_model = opts.model
        fk = get_foreign_key(parent_model, self.model_class)
        return fk.name

    def get_queryset(self, instance):
        if self.queryset:
            if not self.queryset.model == self.model_class:
                raise WrongModelError('%s expected, '
                                      'got %s instead.' % (self.model_class,
                                                           self.queryset.model))
            if not isinstance(self.queryset, QuerySet):
                raise Exception('QuerySet instance expected, '
                                'got %s instead.' % type(self.queryset))
            return self.queryset

        if self.instance_lookup is None:
            # Find the fk from the node class model to the instance model
            self.instance_lookup = self._get_fk_name(instance)
        lookup = {self.instance_lookup: instance}
        if self.filter_lookup:
            lookup.update(self.filter_lookup)
        queryset = self.model_class.objects.filter(**lookup)
        if self.exclude_lookup:
            queryset = queryset.exclude(**self.exclude_lookup)
        return queryset
