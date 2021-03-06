from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType

from grass.admin import GrassAdmin, GrassInlineModelAdmin
from grass.tests.base import *
from grass.tests.models import *


class AssignmentInline(GrassInlineModelAdmin):
    model = Assignment


class WorkerAdmin(GrassAdmin):
    inlines = [
        AssignmentInline,
    ]


class ImproperlyConfiguredAssignmentInline(GrassInlineModelAdmin):
    model = Assignment

    @classmethod
    def get_autocomplete_search_fields(cls):
        return [('^name',)] * 5 # Four expected


class ImproperlyConfiguredWorkerAdmin(GrassAdmin):
    inlines = [
        ImproperlyConfiguredAssignmentInline,
    ]


class NoGFKAssignmentInline(GrassInlineModelAdmin):
    model = NoGFKAssignment


class NoGFKWorkerAdmin(GrassAdmin):
    inlines = [
        NoGFKAssignmentInline
    ]


class MultipleGFKAssignmentInline(GrassInlineModelAdmin):
    model = MultipleGFKAssignment


class MultipleGFKWorkerAdmin(GrassAdmin):
    inlines = [
        MultipleGFKAssignmentInline
    ]


class MultipleGFKWithGFKNameAssignmentInline(GrassInlineModelAdmin):
    model = MultipleGFKAssignment
    gfk_name = 'content_object_1'


class MultipleGFKWithGFKNameWorkerAdmin(GrassAdmin):
    inlines = [
        MultipleGFKWithGFKNameAssignmentInline
    ]


class GFKWrongNameAssignmentInline(GrassInlineModelAdmin):
    model = MultipleGFKAssignment
    gfk_name = 'content_object_3'


class GFKWrongNameGFKWorkerAdmin(GrassAdmin):
    inlines = [
        GFKWrongNameAssignmentInline
    ]


class AdminTest(TestCase):

    fixtures = ['testing_data.json']

    def test_admin(self):
        self.assertIsNone(WorkerAdmin.validate(Worker))

    def test_no_gfk__admin(self):
        self.assertRaises(ImproperlyConfigured, NoGFKWorkerAdmin.validate, Worker)

    def test_multiple_gfk_admin(self):
        self.assertRaises(ImproperlyConfigured, MultipleGFKWorkerAdmin.validate, Worker)

    def test_wrong_gfk_name_admin(self):
        self.assertRaises(ImproperlyConfigured, GFKWrongNameGFKWorkerAdmin.validate, Worker)

    def test_improperly_configured_admin(self):
        self.assertRaises(ImproperlyConfigured, ImproperlyConfiguredWorkerAdmin.validate, Worker)

    def test_multiple_gfk_with_gfk_name_admin(self):
        self.assertIsNone(MultipleGFKWithGFKNameWorkerAdmin.validate(Worker))

    def test_inline_content_type_list(self):
        inline = AssignmentInline
        model_list = (Aisle, Item, Shelf, Warehouse)
        expected = [ContentType.objects.get_for_model(i) for i in model_list]
        self.assertEqual(inline.get_content_type_list(), expected)

    def test_inline_all_content_type_list(self):
        inline = MultipleGFKWithGFKNameAssignmentInline
        expected = set(inline.get_content_type_list())
        self.assertEqual(expected, set(ContentType.objects.all()))

    def test_default_autocomplete_choices(self):
        inline = AssignmentInline
        model_list = (Aisle, Item, Shelf, Warehouse)
        expected = [model._default_manager.all() for model in model_list]
        choices = inline.get_autocomplete_choices()
        for idx, choice in enumerate(choices):
            self.assertQuerysetEqual(choice, map(repr, expected[idx]))

    def test_autocomplete_choices_all_content_types(self):
        inline = MultipleGFKWithGFKNameAssignmentInline
        ct_list = ContentType.objects.all()
        expected = [i.model_class()._default_manager.all() for i in ct_list]
        choices = inline.get_autocomplete_choices()
        for idx, choice in enumerate(choices):
            self.assertQuerysetEqual(choice, map(repr, expected[idx]))

    def test_default_autocomplete_search_fields(self):
        inline = AssignmentInline
        expected = [('^name',)] * 4
        self.assertEqual(expected, inline.get_autocomplete_search_fields())

    def test_autocomplete_search_fields_content_types(self):
        inline = MultipleGFKWithGFKNameAssignmentInline
        ct_list = ContentType.objects.all()
        expected = [('^name',)] * len(ct_list)
        self.assertEqual(expected, inline.get_autocomplete_search_fields())
