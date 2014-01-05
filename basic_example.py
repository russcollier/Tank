#!/usr/bin/python

import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))

from tank.container import Container
from tests.cars import IEngine


class Car:
    """
    @tests.cars.IEngine
    """
    def __init__(self, engine):
        self.__engine = engine

    @property
    def engine(self):
        return self.__engine


def main():
    container = Container()
    container.register('tests.cars.IEngine',
                       'tests.cars.FourCylinder')
    container.register('Car')

    car = container.resolve('Car')
    assert isinstance(car.engine, IEngine)

    print '{0} cylinders'.format(car.engine.number_of_cylinders)
    car.engine.start()


if __name__ == '__main__':
    main()
