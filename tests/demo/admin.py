from django.contrib import admin

from grass.register import grass
from grass.tests.base import WorkerAdmin, WarehouseNode
from grass.tests.models import (
    Warehouse,
    Aisle,
    Shelf,
    Item,
    Worker,
    Assignment,
)

grass.register(WarehouseNode)

admin.site.register(Worker, WorkerAdmin)

admin.site.register(Aisle)
admin.site.register(Shelf)
admin.site.register(Item)
admin.site.register(Warehouse)
admin.site.register(Assignment)
