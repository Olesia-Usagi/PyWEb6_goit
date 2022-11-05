import pickle
import json


# Part 1
class SerializationInterface():

    def serialize(self, file):
        raise NotImplementedError('Не переназначен метод.')  # Создаётся метод-инструкция для наследующих классов


class SerializeToJSON(SerializationInterface):  # Создан класс для сериализации JSON

    def serialize(self, file):  # Наследуем и переопределяем метод родителя-интерфейса
        with open('json_data.json', 'w') as f:
            json.dump(file, f)


class SerializeToBin(SerializationInterface):  # Создан класс для сериализации .bin

    def serialize(self, file):  # Наследуем и переопределяем метод родителя-интерфейса
        with open('bin_data.bin', 'wb') as f:
            pickle.dump(file, f)


class Meta(type):
    children_number = 0

    def __new__(cls, *args, **kwargs):
        print(cls, "__new__ CountingClass called")
        instance = super().__new__(cls, *args, **kwargs)
        instance.class_number = cls.children_number
        cls.children_number = cls.children_number + 1
        return instance


# Part 2

Meta.children_number = 0


class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data


class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data


assert (Cls1.class_number, Cls2.class_number) == (0, 1)
a, b = Cls1(''), Cls2('')
assert (a.class_number, b.class_number) == (0, 1)
