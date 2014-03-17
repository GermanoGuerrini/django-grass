from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ObjectDoesNotExist, ValidationError

class GrassInlineFormSet(BaseInlineFormSet):
    # TODO Should have an hidden widget
    def clean(self):
        super(GrassInlineFormSet, self).clean()
        for form in self.forms:
            cleaned_data = form.cleaned_data
            if cleaned_data and not cleaned_data[u'DELETE']:
                # TODO
                # Check if ct has been tampered
                # Check if object_id is numeric (!)
                ct = cleaned_data['content_type']
                try:
                    ct.get_object_for_this_type(pk=cleaned_data['object_id'])
                except ObjectDoesNotExist:
                    msg = 'Object not found for content_type %s and object_id %s'
                    raise ValidationError(msg % (ct, cleaned_data['object_id']))
