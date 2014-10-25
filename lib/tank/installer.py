from abc import ABCMeta, abstractmethod


class IInstaller:
    __metaclass__ = ABCMeta

    @abstractmethod
    def install(self, container):
        raise Exception("Please a concrete implementation")
