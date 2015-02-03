from django.test import TestCase

from grass.tests.base import WarehouseNode
from grass.tests.models import Warehouse

class NodeTest(TestCase):

    fixtures = ['testing_data.json']

    def test_node(self):
        node = WarehouseNode()
        warehouse = Warehouse.objects.get(pk=1)
        choice_fields = node.choice_fields(warehouse)
        self.assertEqual(len([c for c in choice_fields]), 3)
