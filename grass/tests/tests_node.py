from django.test import TestCase

from .base import *

class NodeTest(TestCase):
    def test_node(self):
        node = WarehouseNode()
        warehouse = Warehouse.objects.get(pk=1)
        choice_fields = node.choice_fields(warehouse)
        self.assertEqual(len(choice_fields), 3)
