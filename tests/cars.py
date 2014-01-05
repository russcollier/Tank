from abc import ABCMeta, abstractmethod


class IEngine:
    __metaclass__ = ABCMeta

    def __init__(self):
        raise NotImplemented('Please use a concrete type')

    @property
    @abstractmethod
    def number_of_cylinders(self):
        pass

    @abstractmethod
    def start(self):
        pass


class FourCylinder(IEngine):
    def __init__(self):
        pass

    @property
    def number_of_cylinders(self):
        return 4

    def start(self):
        print 'vroom'


class SixCylinder(IEngine):
    def __init__(self):
        pass

    @property
    def number_of_cylinders(self):
        return 6

    def start(self):
        print 'VRRROOOOMMM!'
