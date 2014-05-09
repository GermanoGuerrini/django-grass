from django import forms
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden, Http404
from django.db.models.fields import FieldDoesNotExist
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.functional import cached_property

import autocomplete_light

from .exceptions import GenericForeignKeyNotFound, MultipleGenericForeignKeys
from .formsets import GrassInlineFormSet
from .register import grass
from .utils import get_generic_foreign_key


# This ominous monkey patching is due to the impossibility to subclass
# autocomplete_light.AutocompleteGenericBase (I tried as hard as I could)
# I don't know why the variable 'values' MUST be not None in order for the
# widget to work, but I'm sure I'll go to hell for this.
# TODO Submit a pull request?
super_choices_for_values = autocomplete_light.AutocompleteGenericBase.choices_for_values

def choices_for_values(self):
    if self.values is not None:
        return super_choices_for_values(self)
    return []

autocomplete_light.AutocompleteGenericBase.choices_for_values = choices_for_values


class GrassModelAdminValidator(admin.validation.ModelAdminValidator):
    def validate_grass_inline(self, cls, model):
        """
        Checks that all GrassInlineModelAdmin inlines refer to a model with a
        properly configured GenericForeignKey field.
        """
        for idx, inline in enumerate(cls.inlines):
            if issubclass(inline, GrassInlineModelAdmin):
                try:
                    get_generic_foreign_key(inline.model, inline.gfk_name)
                except FieldDoesNotExist:
                    raise ImproperlyConfigured("%s.inlines[%d] " \
                        "is a GrassInlineModelAdmin that refers to " \
                        "gfk_name '%s' that cannot be found on model %r" \
                        % (cls.__name__, idx, inline.gfk_name, inline.model))
                except GenericForeignKeyNotFound:
                    raise ImproperlyConfigured("%s.inlines[%d] "
                        "is a GrassInlineModelAdmin but refers to model %r "
                        "that does not have a GenericForeignKey field."
                        % (cls.__name__, idx, inline.model))
                except MultipleGenericForeignKeys:
                    raise ImproperlyConfigured("%s.inlines[%d] "
                        "is a GrassInlineModelAdmin that refers to model %r "
                        "that has more than one GenericForeignKey field. "
                        "You must specify a gfk_name value to avoid any "
                        "ambiguity."
                        % (cls.__name__, idx, inline.model))


class GrassAdmin(admin.ModelAdmin):

    validator_class = GrassModelAdminValidator

    class Media:
        js = ('admin/grass/core.js',)

    def get_urls(self):
        urls = super(GrassAdmin, self).get_urls()
        grass_urls = patterns('',
            url(r'^selected_choices/$',
                self.admin_site.admin_view(self.selected_choices), name='asd'),
        )
        return grass_urls + urls

    def selected_choices(self, request):
        if request.is_ajax():
            content_type = request.GET.get('content_type')
            object_id = request.GET.get('object_id')
            if content_type and object_id:
                try:
                    ct = ContentType.objects.get_for_id(content_type)
                    model = ct.model_class()
                    node = grass.get_node_for_model(model)
                except Exception, e:
                    print e
                    # TODO List exact exceptions
                    raise Http404

                instance = get_object_or_404(model, pk=object_id)
                choice_fields = node.choice_fields(instance)
                return render_to_response('admin/grass/results.html',
                                          {'fields': choice_fields},
                                          RequestContext(request))
            return HttpResponseForbidden()
        raise Http404


class GrassInlineModelAdmin(admin.options.InlineModelAdmin):
    """
    Inline model admin that build a special form containing a fully configured
    autocomplete_light search field.
    
    # TODO
    The autocomplete_light selection trigger the subsequent forms (MAYBE)
    """
    formset = GrassInlineFormSet
    template = 'admin/grass/inline.html'
    grass_nodes = []
    gfk_name = None
    gfk_label = None
    autocomplete_name = None
    extra = 0

    def __init__(self, *args, **kwargs):
        """
        Registers the autocomplete class at instantiation time.
        """
        super(GrassInlineModelAdmin, self).__init__(*args, **kwargs)
        autocomplete_light.register(self.model, self.get_autocomplete_class())

    @cached_property
    def content_type_list(self):
        """
        Returns a list of all the content types that can be associated to the
        model of this class through the generic foreign key field.
        If the content type field has not been limited, it will returns all the
        content types currently registered.
        """
        gfk_field = get_generic_foreign_key(self.model, self.gfk_name)
        ct_field = self.model._meta.get_field(gfk_field.ct_field)
        return [i for i in ct_field.rel.to._default_manager.complex_filter(
            ct_field.rel.limit_choices_to)]

    def get_autocomplete_choices(self):
        """
        Returns a list of querysets to be used by the autocomplete field.
        By default it returns all the objects for each of the content type of
        the generic foreign key of the inline model.
        If you override this method to change the default behavior be sure to
        override ``get_autocomplete_search_fields`` too to match the number of
        lists returned.
        Beware that when you limit the content types of a foreign key field,
        they will be ordered alphabetically. Keep that in mind when overriding
        ``get_autocomplete_search_fields``.
        Further explanation:
        http://django-autocomplete-light.readthedocs.org/en/v2/generic.html
        """
        ct_list = self.content_type_list
        return [i.model_class()._default_manager.all() for i in ct_list]

    @cached_property
    def autocomplete_choices(self):
        return self.get_autocomplete_choices()

    def get_autocomplete_search_fields(self):
        """
        Returns a list of lists of fields to search in.
        The first list of fields will be used for the first queryset in choices
        and so on.
        By defaults it returns a list containing a field named 'name' for each
        queryset.
        Subclasses can override this method.
        Further explanation:
        http://django-autocomplete-light.readthedocs.org/en/v2/generic.html
        """
        return [('name',)] * len(self.autocomplete_choices)

    @cached_property
    def autocomplete_search_fields(self):
        return self.get_autocomplete_search_fields()

    def _get_autocomplete_name(self):
        """
        Internally, the class uses this method to retrieve the
        `autocomplete_name` so that we can set a sensible default.
        Using a metaclass would have been much more elegant, but subclassing a
        django class with all its metaclasses is a pain in the butt and not
        future proof.
        """
        if self.autocomplete_name is None:
            self.autocomplete_name = '%sAutocomplete' % self.model.__name__
        return self.autocomplete_name

    def _get_gfk_label(self):
        """
        See _get_autocomplete_name doc.
        """
        if self.gfk_label is None:
            gfk_field = get_generic_foreign_key(self.model, self.gfk_name)
            self.gfk_label = gfk_field.name
        return self.gfk_label.capitalize()

    def get_autocomplete_class(self):
        """
        Returns a configured AutocompleteGenericBase subclass to be used in the
        generic model choice field of the grass form.
        """
        return type(self._get_autocomplete_name(),
                    (autocomplete_light.AutocompleteGenericBase,),
                    dict(choices=self.autocomplete_choices,
                         search_fields=self.autocomplete_search_fields))

    def get_form_gfk_name(self):
        """
        Returns the name for the autocomplete field used in the form.
        """
        return '%s_fk' % self.model.__name__.lower()

    def get_grass_form(self):
        """
        Returns a form with a single autocomplete field.
        """
        generic_fk_name = self.get_form_gfk_name()
        return type('GrassForm', (forms.Form,), {
                    generic_fk_name: autocomplete_light.GenericModelChoiceField(
                        self._get_autocomplete_name(),
                        label=self._get_gfk_label())})()

