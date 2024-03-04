from collections import UserDict

class CaseInsensitiveDict(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__()  # Инициализируем базовый класс без аргументов сначала
        # Преобразуем все переданные ключи в нижний регистр
        for key, value in dict(*args, **kwargs).items():
            self.data[key.lower()] = value

    def __getitem__(self, key):
        return super().__getitem__(key.lower())

    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)

    def __delitem__(self, key):
        super().__delitem__(key.lower())

    def __contains__(self, key):
        return super().__contains__(key.lower())

my_dict = CaseInsensitiveDict({'Name': 'John', 'Age': 30})
print(my_dict['name'])
print(my_dict['age'])
my_dict['Gender'] = 'Male'
print(my_dict['GENDER'])