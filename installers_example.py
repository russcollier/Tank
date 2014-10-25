#!/usr/bin/python

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))

from tank.container import Container
from tests.installers import InstallerForTest, InstallerForProd, ISendTheMessage

def main():
    container = Container()
    container.install(InstallerForProd())

    sender = container.resolve('tests.installers.ISendTheMessage')
    assert isinstance(sender, ISendTheMessage)

    print(sender.send_message())

    container = Container()
    container.install(InstallerForTest())

    sender = container.resolve('tests.installers.ISendTheMessage')
    assert isinstance(sender, ISendTheMessage)

    print(sender.send_message())

if __name__ == '__main__':
    main()
