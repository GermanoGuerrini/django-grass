from django import forms
from django.db.models.query import QuerySet

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
        queryset = self.get_queryset(instance)
        return self.field_class(queryset=queryset)
    
    def _get_fk_name(self, instance):
        opts = instance._meta
        parent_model = opts.model
        fk = get_foreign_key(parent_model, self.model_class)
        return fk.name
    
    def get_queryset(self, instance):
        if self.queryset:
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
    
