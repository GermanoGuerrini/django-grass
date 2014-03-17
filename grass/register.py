from .exceptions import ModelNotRegistered, ModelAlreadyRegistered

class Register(object):
    """
    Register class.
    """
    def __init__(self):
        self._registry = {}
    
    def get_node_for_model(self, model):
        """
        Returns a node for the given *model*. If the model has not been
        registered, it raises a *ModelNotRegistered* exception.
        """
        try:
            return self._registry[model]
        except KeyError:
            raise ModelNotRegistered('Model %s is not registered' % model)
    
    def register(self, model, node_class, children=None):
        """
        Registers a model to be handled by *node_class*.
        """
        if model in self._registry:
            raise ModelAlreadyRegistered(
                "The model %s is already registered." % 
                model._meta.module_name)
        node = node_class(model, children)
        self._registry[model] = node

    def unregister(self, model):
        """ Do not use it. Just for testing, really. """
        if model in self._registry:
            del self._registry[model]

grass = Register()