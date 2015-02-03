from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models


class BaseModel(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        abstract = True
        ordering = ['name']


class Warehouse(BaseModel):
    pass


class Aisle(BaseModel):
    warehouse = models.ForeignKey(Warehouse)


class Shelf(BaseModel):
    aisle = models.ForeignKey(Aisle)


class Item(BaseModel):
    shelf = models.ForeignKey(Shelf)


class Worker(BaseModel):
    pass


CT_WORKER_CHOICES = models.Q(app_label='tests', model='warehouse') | \
                    models.Q(app_label='tests', model='shelf') | \
                    models.Q(app_label='tests', model='aisle') | \
                    models.Q(app_label='tests', model='item')

class Assignment(models.Model):
    worker = models.ForeignKey(Worker, related_name='assignments')
    content_type = models.ForeignKey(ContentType,
        limit_choices_to=CT_WORKER_CHOICES, related_name='+')
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return u'{0} assigned to {1}'.format(self.worker, self.content_object)


class NoGFKAssignment(models.Model):
    worker = models.ForeignKey(Worker, related_name='+')


class MultipleGFKAssignment(models.Model):
    worker = models.ForeignKey(Worker, related_name='+')

    content_type_1 = models.ForeignKey(ContentType, related_name='+')
    object_id_1 = models.PositiveIntegerField()
    content_object_1 = generic.GenericForeignKey("content_type_1", "object_id_1")

    content_type_2 = models.ForeignKey(ContentType, related_name='+')
    object_id_2 = models.PositiveIntegerField()
    content_object_2 = generic.GenericForeignKey("content_type_2", "object_id_2")
