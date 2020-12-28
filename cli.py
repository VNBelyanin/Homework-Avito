import click
from random import random
import doctest


class SizeMixin:
    proportion = {'XL': 2, 'L': 1}

    def __eq__(self, other):

        """Сравнивает размеры двух пицц"""

        return self.size == other.size


class Margherita(SizeMixin):
    structure = {'tomato sauce': (100, 'г'),
                 'mozzarella': (200, 'г'),
                 'tomatoes': (2, 'шт')}

    def __init__(self, size: str = 'L'):

        """Создание пиццы маргарита"""

        self.size = size

    def dict(self):

        """Выдает рецепт для пиццы маргарита определенного размера"""

        calc_structure = {i: str(self.structure[i][0] * self.proportion[self.size]) +
                          self.structure[i][1]
                          for i in self.structure}
        return {'Margherita': calc_structure}


class Pepperoni(SizeMixin):
    structure = {'tomato sauce': (50, 'г'),
                 'mozzarella': (150, 'г'),
                 'pepperoni': (10, 'кусочков')}

    def __init__(self, size: str = 'L'):

        """Создание пиццы пепперони"""
        self.size = size

    def dict(self):

        """Выдает рецепт для пиццы пепперони определенного размера"""

        calc_structure = {i: str(self.structure[i][0] * self.proportion[self.size]) +
                          self.structure[i][1]
                          for i in self.structure}
        return {'Pepperoni': calc_structure}


@click.group()
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool) -> None:

    """Готовит и доставляет пиццу"""

    print(bake(pizza))
    if delivery is True:
        print(_delivery(pizza))
    else:
        print(pickup(pizza))


@cli.command()
def menu() -> None:

    """Выводит меню"""

    print('У нас есть пиццы двух размеров: L и XL')
    for i in SizeMixin.__subclasses__():
        print(i.__name__, tuple(i.structure))


def log(param: str = 'Приготовили за {} мин'):
    def outer_func(func):
        def timer(pizza: str):
            func(pizza)
            t = round(30 * random()) + 1
            return param.format(t)
        return timer
    return outer_func


@log()
def bake(pizza: str) -> None:

    """Готовит пиццу
    >>> bake('name')
    начали готовить name"""

    print('начали готовить', pizza)


@log('Доставили за {} мин!')
def _delivery(pizza: str) -> None:

    """Доставляет пиццу
    >>> _delivery('name')
    name передана курьеру"""
    print(pizza, 'передана курьеру')


@log('Забрали за {} мин!')
def pickup(pizza: str) -> None:

    """Самовывоз
    >>> pickup ('name')
    name ожидает получения"""

    print(pizza, 'ожидает получения')


if __name__ == "__main__":
    cli()
    doctest.testmod()
