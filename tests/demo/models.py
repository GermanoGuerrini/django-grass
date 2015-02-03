from grass.tests.models import (
    Warehouse,
    Aisle,
    Shelf,
    Item,
    Worker,
    Assignment,
)
# from django.db import models
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes import generic
#
#
# class BaseModel(models.Model):
#     name = models.CharField(max_length=64)
#
#     def __unicode__(self):
#         return unicode(self.name)
#
#     class Meta:
#         abstract = True
#         ordering = ['name']
#
#
# class Warehouse(BaseModel):
#     pass
#
#
# class Aisle(BaseModel):
#     warehouse = models.ForeignKey(Warehouse)
#
#
# class Shelf(BaseModel):
#     aisle = models.ForeignKey(Aisle)
#
#
# class Item(BaseModel):
#     shelf = models.ForeignKey(Shelf)
#
#
# class Worker(BaseModel):
#     pass
#
#
# CT_WORKER_CHOICES = models.Q(app_label='demo', model='warehouse') | \
#                     models.Q(app_label='demo', model='shelf') | \
#                     models.Q(app_label='demo', model='aisle') | \
#                     models.Q(app_label='demo', model='item')
#
# class Assignment(models.Model):
#     worker = models.ForeignKey(Worker, related_name='assignments')
#     content_type = models.ForeignKey(ContentType,
#         limit_choices_to=CT_WORKER_CHOICES, related_name='+')
#     object_id = models.PositiveIntegerField()
#     content_object = generic.GenericForeignKey()
#
#     def __unicode__(self):
#         return u'{0} assigned to {1}'.format(self.worker, self.content_object)
