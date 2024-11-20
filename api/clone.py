from furniture.models import Furniture
from random import randint, choice


def clone_furniture(count):
    arr = []
    furniture2 = Furniture.objects.first()

    for i in range(count):
        furniture = furniture2

        furniture.id = None
        furniture.price = randint(10000, 40000)

        furniture.save()
        arr.append(furniture)

    return arr
