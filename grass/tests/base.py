from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from ..forms import BaseNode, MultipleChoiceFieldFactory

from demo.models import models as django_models
from demo.models import (
    Worker,
    Item,
    Aisle,
    Shelf,
    Warehouse,
    Assignment
)


class NoGFKAssignment(django_models.Model):
    worker = django_models.ForeignKey(Worker, related_name='+')


class MultipleGFKAssignment(django_models.Model):
    worker = django_models.ForeignKey(Worker, related_name='+')
    
    content_type_1 = django_models.ForeignKey(ContentType)
    object_id_1 = django_models.PositiveIntegerField()
    content_object_1 = generic.GenericForeignKey("content_type_1", "object_id_1")
    
    content_type_2 = django_models.ForeignKey(ContentType)
    object_id_2 = django_models.PositiveIntegerField()
    content_object_2 = generic.GenericForeignKey("content_type_2", "object_id_2")


class ItemNode(BaseNode):
    model = Item


class AisleNode(BaseNode):
    model = Aisle


class ShelfNode(BaseNode):
    model = Shelf


class WarehouseNode(BaseNode):
    model = Warehouse
    fields = (
        MultipleChoiceFieldFactory(Aisle), 
        MultipleChoiceFieldFactory(Shelf, 'aisle__warehouse'),
        MultipleChoiceFieldFactory(Item, queryset=Item.objects.filter(pk__in=(1,2,3)))
    )