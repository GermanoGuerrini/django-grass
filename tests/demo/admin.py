from django.contrib import admin

from grass.admin import GrassAdmin, GrassInlineModelAdmin
from grass.forms import MultipleChoiceFieldFactory, BaseNode
from grass.register import grass

from demo.models import (
    Warehouse,
    Aisle,
    Shelf,
    Item,
    Worker,
    Assignment,
)

class WarehouseNode(BaseNode):
    model = Warehouse
    fields = (
        MultipleChoiceFieldFactory(Aisle), 
        MultipleChoiceFieldFactory(Shelf, 'aisle__warehouse'),
        MultipleChoiceFieldFactory(Item, queryset=Item.objects.filter(pk__in=(1,2,3)))
    )

grass.register(WarehouseNode)


class AssignmentInline(GrassInlineModelAdmin):
    gfk_label = 'assigned to'
    model = Assignment
    grass_nodes = [
        WarehouseNode,
    ]


class WorkerAdmin(GrassAdmin):
    inlines = [
        AssignmentInline,
    ]

admin.site.register(Worker, WorkerAdmin)

admin.site.register(Aisle)
admin.site.register(Shelf)
admin.site.register(Item)
admin.site.register(Warehouse)
admin.site.register(Assignment)
