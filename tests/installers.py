from abc import ABCMeta, abstractmethod
from tank.installer import IInstaller


class ICreateTheMessage:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_message(self):
        raise Exception("Please a concrete implementation")


class TheMessageProvider(ICreateTheMessage):
    def get_message(self):
        return "This is the REAL PRODUCTION message"


class ISendTheMessage:
    __metaclass__ = ABCMeta

    @abstractmethod
    def send_message(self):
        raise Exception("Please a concrete implementation")


class MockMessageSender(ISendTheMessage):
    def send_message(self):
        return "TESTING This is a test message"


class RealMessageSender(ISendTheMessage):
    """
    @tests.installers.ICreateTheMessage
    """
    def __init__(self, message_creator):
        assert isinstance(message_creator, ICreateTheMessage)
        self.__message_creator = message_creator

    def send_message(self):
        return self.__message_creator.get_message()


class AbstractInstaller():
    def get_message_sender(self):
        pass


class InstallerForTest(AbstractInstaller, IInstaller):
    def install(self, container):
        container.register('tests.installers.ISendTheMessage', 'tests.installers.MockMessageSender')


class InstallerForProd(AbstractInstaller, IInstaller):
    def install(self, container):
        container.register('tests.installers.ICreateTheMessage', 'tests.installers.TheMessageProvider')
        container.register('tests.installers.ISendTheMessage', 'tests.installers.RealMessageSender')
