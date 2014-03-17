from django.test import TestCase

from .base import *

class MultipleChoiceFieldFactoryTest(TestCase):
    
    def test_simple(self):
        field = MultipleChoiceFieldFactory(Aisle)
        warehouse = Warehouse.objects.get(pk=1)
        qs = field.get_queryset(warehouse)
        expected = Aisle.objects.filter(warehouse=warehouse)
        self.assertQuerysetEqual(qs, map(repr, expected))
    
    def test_fail_get_fk(self):
        field = MultipleChoiceFieldFactory(Shelf)
        warehouse = Warehouse.objects.get(pk=1)
        self.assertRaises(Exception, field.get_queryset, warehouse)
    
    def test_instance_lookup(self):
        field = MultipleChoiceFieldFactory(Shelf, 'aisle__warehouse')
        warehouse = Warehouse.objects.get(pk=1)
        qs = field.get_queryset(warehouse)
        expected = Shelf.objects.filter(aisle__warehouse=warehouse)
        self.assertQuerysetEqual(qs, map(repr, expected))
    
    def test_filter_lookup(self):
        field = MultipleChoiceFieldFactory(Aisle, filter_lookup={'name__contains': 2})
        warehouse = Warehouse.objects.get(pk=1)
        qs = field.get_queryset(warehouse)
        expected = Aisle.objects.filter(warehouse=warehouse, name__contains=2)
        self.assertQuerysetEqual(qs, map(repr, expected))
    
    def test_exclude_lookup(self):
        field = MultipleChoiceFieldFactory(Aisle, exclude_lookup={'name__contains': 2})
        warehouse = Warehouse.objects.get(pk=1)
        qs = field.get_queryset(warehouse)
        expected = Aisle.objects.filter(warehouse=warehouse).exclude(name__contains=2)
        self.assertQuerysetEqual(qs, map(repr, expected))
    
    def test_custom_queryset(self):
        field = MultipleChoiceFieldFactory(Aisle, queryset=Aisle.objects.filter(pk__in=(1, 2)))
        warehouse = Warehouse.objects.get(pk=1)
        qs = field.get_queryset(warehouse)
        expected = Aisle.objects.filter(pk__in=(1, 2))
        self.assertQuerysetEqual(qs, map(repr, expected))
    
    def test_wrong_queryset(self):
        field = MultipleChoiceFieldFactory(Aisle, queryset=Aisle.objects.get(pk=2))
        warehouse = Warehouse.objects.get(pk=1)
        self.assertRaises(Exception, field.get_queryset, warehouse)
