from django.utils.text import slugify

import autocomplete_light

from grass import settings


class GrassAutocompleteGenericBase(autocomplete_light.AutocompleteGenericBase):
    choices = ()
    search_fields = ()
    autocomplete_js_attributes = {
        'minimum_characters': settings.AUTOCOMPLETE_MIN_CHARS,
    }

    def _get_model_name_and_q(self):
        """
        Extracts the name of the model used to filter the queryset from the
        query string and returns them both.
        """
        model_name = None
        q = self.request.GET.get('q', '')
        words = q.split()
        if len(words) >= 2 and words[0].startswith('@'):
            model_name = words[0][1:]
            q = ' '.join(words[1:])
        return model_name, q

    def _choices_for_request_conditions(self, q, search_fields):
        """
        Strips the name of the model used to filter the queryset from the
        query string.
        """
        _, q = self._get_model_name_and_q()
        return super(GrassAutocompleteGenericBase, self
                     )._choices_for_request_conditions(q, search_fields)

    def choices_for_request(self):
        """
        Allows users to filter the queryset list by model.
        """
        model_name, _ = self._get_model_name_and_q()
        if model_name is not None:
            choices = []
            for queryset in self.choices:
                model_meta = queryset.model._meta
                name = model_meta.model_name
                verbose_name = unicode(model_meta.verbose_name)
                slug = slugify(verbose_name).replace('-', '')
                if model_name == name or model_name == slug:
                    choices.append(queryset)
            if choices:
                self.choices = choices

        return super(GrassAutocompleteGenericBase, self).choices_for_request()
