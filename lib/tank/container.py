import inspect
import logging
import sys
from abc import ABCMeta, abstractmethod


from tank.exception import ComponentNotFoundException


class IContainer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def register(self, interface, implementation=None, factory_method=None):
        raise NotImplementedError('Please a concrete implementation')


class Container(IContainer):
    Log = logging.getLogger(__name__)

    def __init__(self):
        self.__registrations = dict()
        self.__instances = dict()

    def install(self, *installers):
        for installer in installers:
            installer.install(self)

    def register(self, interface, implementation=None, factory_method=None):
        if implementation or factory_method:
            if implementation:
                self.__registrations[interface] = implementation
            if factory_method:
                self.__registrations[interface] = factory_method()
        else:
            self.__registrations[interface] = interface

    def resolve(self, type_name):
        self.Log.info("Resolving type: '{0}'".format(type_name))

        if type_name not in self.__registrations.keys():
            raise ComponentNotFoundException('Unable to resolve type {0} - no registrations found'.format(type_name))

        implementation_type_name = self.__registrations[type_name]
        module = '__main__'
        class_name = implementation_type_name

        need_to_create_implementation = False

        if isinstance(implementation_type_name, str):
            need_to_create_implementation = True
            if '.' in implementation_type_name:
                module = implementation_type_name.rsplit('.', 1)[0]
                class_name = implementation_type_name.rsplit('.', 1)[1]

            __import__(module, fromlist=class_name)
            module = sys.modules[module]
            class_object = getattr(module, class_name)
        elif inspect.isclass(implementation_type_name):
            need_to_create_implementation = True
            class_object = implementation_type_name
        else:
            class_object = implementation_type_name

        docs = class_object.__doc__
        args = []

        if docs:
            for line in docs.split('\n'):
                line = line.strip()
                if line is None or line == '' or line[0] != '@':
                    continue
                type_name = line[1:]
                args.append(self.resolve(type_name))

        if class_name not in self.__instances.keys():
            if need_to_create_implementation:
                if len(args) > 0:
                    instance = class_object(*args)
                else:
                    instance = class_object()
            else:
                instance = class_object
            self.__instances[class_name] = instance

        return self.__instances[class_name]
