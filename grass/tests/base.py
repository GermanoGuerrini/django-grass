from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from grass.forms import BaseNode, MultipleChoiceFieldFactory

from grass.tests.models import (
    Worker,
    Item,
    Aisle,
    Shelf,
    Warehouse,
    Assignment
)


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
