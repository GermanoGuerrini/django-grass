from django.contrib.contenttypes.generic import GenericForeignKey
from django.db.models.fields import FieldDoesNotExist

from .exceptions import GenericForeignKeyNotFound, MultipleGenericForeignKeys

def get_generic_foreign_key(model, gfk_name=None):
    opts = model._meta
    virtual_fields = opts.virtual_fields
    if gfk_name:
        for f in virtual_fields:
            if f.name == gfk_name:
                return f
        raise FieldDoesNotExist('%s has no field named %s' % (model, gfk_name))
    candidates = [f for f in virtual_fields if isinstance(f, GenericForeignKey)]
    candidates_count = len(candidates)
    if candidates_count == 1:
        return candidates[0]
    if candidates_count == 0:
        raise GenericForeignKeyNotFound('Model %r does not have a '
                                        'GenericForeignKey field')
    raise MultipleGenericForeignKeys('Model %r has more the one '
                                     'GenericForeignKey field')

def get_foreign_key(parent_model, model, fk_name=None, can_fail=False):
    """
    Adapted from django.forms.formsets
    Finds and returns the ForeignKey from model to parent if there is one
    (returns None if can_fail is True and no such field exists). If fk_name is
    provided, assume it is the name of the ForeignKey field. Unless can_fail is
    True, an exception is raised if there is no ForeignKey from model to
    parent_model.
    """
    # avoid circular import
    from django.db.models import ForeignKey
    opts = model._meta
    if fk_name:
        fks_to_parent = [f for f in opts.fields if f.name == fk_name]
        if len(fks_to_parent) == 1:
            fk = fks_to_parent[0]
            if not isinstance(fk, ForeignKey) or \
                    (fk.rel.to != parent_model and
                     fk.rel.to not in parent_model._meta.get_parent_list()):
                raise Exception("fk_name '%s' is not a ForeignKey to %s" % (fk_name, parent_model))
        elif len(fks_to_parent) == 0:
            raise Exception("%s has no field named '%s'" % (model, fk_name))
    else:
        # Try to discover what the ForeignKey from model to parent_model is
        fks_to_parent = [
            f for f in opts.fields
            if isinstance(f, ForeignKey)
            and (f.rel.to == parent_model
                or f.rel.to in parent_model._meta.get_parent_list())
        ]
        if len(fks_to_parent) == 1:
            fk = fks_to_parent[0]
        elif len(fks_to_parent) == 0:
            if can_fail:
                return
            raise Exception("%s has no ForeignKey to %s" % (model, parent_model))
        else:
            raise Exception("%s has more than 1 ForeignKey to %s" % (model, parent_model))
    return fk