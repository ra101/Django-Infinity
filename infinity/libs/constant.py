class ConstantMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        obj = super().__new__(cls, clsname, bases, clsdict)
        obj.__force_set__("__values__", [])
        obj.__force_set__("__keys__", [])
        for key, value in vars(obj).items():
            if not key.startswith("__"):
                obj.__values__.append(value)
                obj.__keys__.append(key)
        obj.__force_set__("keys", lambda: obj.__keys__)
        obj.__force_set__("values", lambda: obj.__values__)
        return obj

    def __force_set__(self, name, value):
        return super().__setattr__(name, value)

    def __setattribute__(self, *args, **kwargs):
        pass

    def __setattr__(self, *args, **kwargs):
        pass

    def __setitem__(self, *args, **kwargs):
        pass

    def __set__(self, *args, **kwargs):
        pass

    def __getitem__(cls, key):
        return getattr(cls, key)

    def __iter__(cls):
        return zip(cls.__keys__, cls.__values__)


class ConstantClass(metaclass=ConstantMeta):
    pass
