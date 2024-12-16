# common/registry.py

class Registry:
    """
    A central registry to manage and retrieve functions by name.
    """
    _registry = {}

    @classmethod
    def register(cls, name):
        """
        Decorator to register a function in the registry with the given name.
        """
        def decorator(func):
            cls._registry[name] = func
            return func
        return decorator

    @classmethod
    def get_function(cls, name):
        """
        Retrieve a function by its name.
        """
        if name not in cls._registry:
            available_functions = ", ".join(cls._registry.keys())
            raise ValueError(f"Function '{name}' is not registered.Available functions: {available_functions}")
        func_or_class = cls._registry[name]
        if isinstance(func_or_class, type):
            return func_or_class()
        return func_or_class
