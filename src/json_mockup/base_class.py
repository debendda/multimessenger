from json import dumps
import inspect

class BaseClass:

    def to_json(self, indent = None):
        return dumps(self, default=lambda x : x.to_dict(), indent=indent)

    def to_dict(self):
        d = {}
        for name in dir(self):
            value = getattr(self, name)
            
            if not name.startswith('__') and not inspect.ismethod(value) and value is not None:

                #check if there are objects of type BaseClass in lists, so we can call to_dict again
                #without this, we will get an error, if objects are in lists because they are not serializable
                if type(value) is list and self.__contains_type(value, BaseClass):
                    d[name] = []
                    for x in value:
                        d[name].append(x.to_dict())
                        
                #also we have to check, if it is an instance and call to_dict again
                elif isinstance(value, BaseClass):
                    d[name] = value.to_dict()

                else:
                    d[name] = value
        return d

    def __contains_type(self, list, type):
        if not list or list == 0:
            return False

        for x in list:
            if isinstance(x, type):
                return True
        return False
