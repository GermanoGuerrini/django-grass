from django.conf import settings


AUTOCOMPLETE_MIN_CHARS = getattr(settings, 'GRASS_AUTOCOMPLETE_MIN_CHARS', 2)
