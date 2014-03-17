from django.core.management.base import BaseCommand

from demo.models import (
    Warehouse,
    Aisle,
    Shelf,
    Item,
    Worker,
)

class Command(BaseCommand):
    help = 'Creates a few objects for the demo application.'

    def handle(self, *args, **options):
        self.stdout.write('Creating objects...')
        for i in ('A', 'B', 'C'):
            warehouse_name = 'Warehouse %s' % i
            warehouse = Warehouse(name=warehouse_name)
            warehouse.save()
            for j in range(100)[1:]:#('1', '2', '3'):
                aisle_name = 'Aisle %s - W%s' % (j, i)
                aisle = Aisle(name=aisle_name, warehouse=Warehouse.objects.get(name=warehouse_name))
                aisle.save()
                for k in range(100)[1:]:#('1', '2', '3'):
                    shelf_name = 'Shelf %s - A%s - W%s' % (k, j, i)
                    shelf = Shelf(name=shelf_name, aisle=Aisle.objects.get(name=aisle_name))
                    shelf.save()
                    for w in ('a', 'b', 'c', 'd', 'e'):
                        item_name = 'Item %s - S%s - A%s - W%s' % (w, k, j, i)
                        it = Item(name=item_name, shelf=Shelf.objects.get(name=shelf_name))
                        it.save()
        for name in ('John', 'Paul', 'Richard', 'George'):
            worker = Worker(name=name)
            worker.save()
        self.stdout.write('Done')
