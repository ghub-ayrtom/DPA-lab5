import csv  # Библиотека импорта и экспорта для электронных таблиц и баз данных
import datetime


# Родительский класс "Человек"
class Person:
    # Метод инициализации экземпляров класса после их создания
    def __init__(self, name, age, gender):
        self.__name = name
        self.__age(age)
        self.__gender = gender

    def __age(self, value):
        if value <= 120:
            self.__age = value

    # Статические метод проверки на совершеннолетие
    @staticmethod
    def is_adult(age):
        return age >= 18

    # Метод (сеттер) для получения имени человека (пользователя)
    def setName(self, newName):
        self.__name = newName

    # Метод (сеттер) для получения возраста человека (пользователя)
    def setAge(self, newAge):
        if newAge <= 120:
            self.__age = newAge

    # Метод (сеттер) для получения пола человека (пользователя)
    def setGender(self, newGender):
        if (newGender == "Male") or (newGender == "Female"):
            self.__gender = newGender

    # Метод (геттер) для изменения имени человека (пользователя)
    def getName(self):
        return self.__name

    # Метод (геттер) для изменения возраста человека (пользователя)
    def getAge(self):
        return self.__age

    # Метод (геттер) для изменения пола человека (пользователя)
    def getGender(self):
        return self.__gender


# Дочерний класс "Пользователь", наследованный от родительского класса "Человек"
class User(Person):
    def __init__(self, name, age, gender, id, date, time, online):
        Person.__init__(self, name, age, gender)
        self.__id = id
        self.__visits = []
        self.login(date)
        self.__time = time
        self.__online = online

    # Метод, который вызывается при новом посещении пользователем Интернет-магазина
    def login(self, date):
        self.__visits.append(date)

    # Кастомный итератор класса (описание ниже)
    def __iter__(self):
        return UserDateIterator(self.__visits)

    # Переопределённый метод вывода информации об объекте класса "Пользователь"
    def __repr__(self):
        # Если сегодня пользователь заходил на сайт
        if (datetime.datetime.now().strftime("%d.%m.%Y") == self.__visits[len(self.__visits) - 1]):
            # Значит он онлайн (время не учитывается)
            return f"{self.__id}. Name = {self.getName()}, age = {self.getAge()} - ONLINE (Log in at {self.__time})"
        else:
            # Иначе он оффлайн (выводим, когда пользователь заходил на сайт крайний раз)
            return f"{self.__id}. Name = {self.getName()}, age = {self.getAge()} - OFFLINE (Last online - {self.__visits[len(self.__visits) - 1]}, {self.__time})"

    # Генератор для перебора списка посещений пользователем Интернет-магазина
    def generator(self, i):
        while i < len(self.__visits):
            yield self.__visits[i]  # Ключевое слово yield возвращает нас обратно в этот метод, запоминая состояние выхода
            i += 1
        else:
            yield 0

    # Метод присвоения значения value какому-либо атрибуту key объекта класса "Пользователь"
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    # Метод позволяет получить значение какого-либо атрибута объекта класса "Пользователь" по его индексу
    def __getitem__(self, item):
        s = "_User__" + item
        return self.__dict__[s]


# Класс кастомного итератора для класса "Пользователь"
class UserDateIterator():
    # При создании итератора, получаем список посещений пользователем Интернет-магазина и инициализируем счётчик для его обхода
    def __init__(self, visits):
        self.visits = visits
        self.i = 0

    # Метод возвращает следующий элемент из списка посещений
    def __next__(self):
        if self.i < len(self.visits):
            date = self.visits[self.i]
            self.i += 1
            return date
        else:
            return 0


fI = open("C:\\Users\\Admin\\PycharmProjects\\DPA\\lab4\\data.csv", 'r')  # Открываем файл для чтения (read)
# Класс DictReader модуля csv создаёт объект, который работает как обычный reader(), но отображает информацию о каждой строке в качестве словаря dict
reader = csv.DictReader(fI, fieldnames = None, restkey = None, restval = None, dialect = "excel")

l = []

for row in reader:
    # Создаём объект класса пользователя и добавляем его в список
    a = User(row["Name"], int(row["Age"]), row["Gender"], int(row['N']), row["Date"], row["Time"], row["Online"])
    l.append(a)

print("Исходные данные: ")
print(l)

l[2].setAge(17)

l[2].login("17.02.2023")

print(l)
print()

# Сортируем список при помощи лямбда-функции по столбцу с именем из таблицы
sSL = sorted(l, key = lambda d: d.getName())
# Сортируем список при помощи лямбда-функции по столбцу с номером клиента из таблицы и переворачиваем список (reverse)
nSL = sorted(l, key = lambda d: d['id'], reverse = True)

print("Сортировка по строковому полю (имени): ")
print(sSL)
print("Сортировка по числовому полю (номеру посетителя) в обратном порядке (reverse): ")
print(nSL)

newL = []

# Отбор посетителей по совершеннолетию (только те, кому больше 17 лет)
newL = list(filter(lambda x: x.is_adult(x.getAge()), l))
print("Совершеннолетние пользователи: ")
print(newL)

# Создаём файл для записи
with open("C:\\Users\\Admin\\PycharmProjects\\DPA\\lab4\\output.csv", 'w', newline = '') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = reader.fieldnames)  # Класс writer служит для записи данных в файл
    writer.writeheader()  # Записываем заголовок таблицы

    for row in sSL:
        d = {}
        d['N'] = row['id']  # Доступ к элементам коллекции по индексу осуществляется при помощи метода __getitem__
        d['Date'] = row['visits'][-1]
        d['Time'] = row['time']
        d['Online'] = row['online']
        d['Gender'] = row.getGender()
        d['Age'] = row.getAge()
        d['Name'] = row.getName()

        # Метод writerow записывает словарь со значениями в файл
        writer.writerow(d)

    for row in nSL:
        d = {}
        d['N'] = row['id']

        # Запись даты через итератор класса
        iterator = iter(row)
        b = next(iterator)
        d['Date'] = str(b)

        while (b):
            b = next(iterator)

            if (b != 0):
                d['Date'] = str(b)
        #

        d['Time'] = row['time']
        d['Online'] = row['online']
        d['Gender'] = row.getGender()
        d['Age'] = row.getAge()
        d['Name'] = row.getName()

        writer.writerow(d)

    for row in newL:
        d = {}
        d['N'] = row['id']

        # Запись даты через генератор класса
        i = 0

        generator = row.generator(i)
        b = next(generator)
        d['Date'] = str(b)

        while (b):
            b = next(generator)

            if (b != 0):
                d['Date'] = str(b)
        #

        d['Time'] = row['time']
        d['Online'] = row['online']
        d['Gender'] = row.getGender()
        d['Age'] = row.getAge()
        d['Name'] = row.getName()

        writer.writerow(d)

print()
print("Пожалуйста, проверьте выходной файл")