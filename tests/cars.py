from abc import ABCMeta, abstractmethod


class IEngine:
    __metaclass__ = ABCMeta

    # noinspection PyPropertyDefinition
    @property
    @abstractmethod
    def number_of_cylinders(self):
        raise NotImplemented('Please use a concrete type')

    @abstractmethod
    def start(self):
        raise NotImplemented('Please use a concrete type')


class FourCylinder(IEngine):
    def __init__(self):
        super().__init__()

    @property
    def number_of_cylinders(self):
        return 4

    def start(self):
        print('vroom')


class SixCylinder(IEngine):
    def __init__(self):
        super().__init__()

    @property
    def number_of_cylinders(self):
        return 6

    def start(self):
        print('VRRROOOOMMM!')
