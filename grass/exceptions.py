class GrassException(Exception): pass

class GenericForeignKeyNotFound(GrassException): pass
class MultipleGenericForeignKeys(GrassException): pass

class ModelAlreadyRegistered(GrassException): pass
class ModelNotRegistered(GrassException): pass