# a = 1
# b = "Hello"
# #
# print(a, b)
#
# c = int(input("Input number: "))
#
# print(a + c)
# print(a - c)
# print(a / c)
# print(a * c)
# print(a // c)
# print(a % c)
# print(a ** c)
#
# print(f"{a}{b}")
# print(str(a)+b)

# a += 1
# a = a + 1

# for i in range(10):
#     print(i)
#
# for i in range(2, 10):
#     print(i)
#
# for i in range(3, 10, 2):
#     print(i)

# for i in range(10):
#     for j in range(10):
#         print(i, j)


# i = 0
# while i < 10:
#     print(i)
#     i += 1


# i = input("letter: ")
# while i != "r":
#     print("FU!")
#     i = input("letter: ")
#
# while True:
#     i = input("letter: ")
#     if i != "r":
#         print("FU!")
#     else:
#         break


# if a > b:
#     print(a)
#
# if (a < b or b < a) and (a < b or b < a):
#     pass
#
# if a < b or b < a:
#     pass


# my_list = ["Hello", 10, 0.1, True]
#
# matrix = [[1, 2, 3], [4, 5, 6, 7]]
# for i in range(len(matrix)):
#     for j in range(len(matrix[i])):
#         print(matrix[i][j], end="\n")
#
# print("hello\nworld")

# import re
#
# row = "rgearggre dddd@Wrregr.fefw fewfwefwe dd@dd.dd dfghjk"
#
# print(re.findall(r"\w+@\w+\.\w+", row))

# a = []
# a.append("dwdw")
# a.append("2")
# print(a)
# print(a[0])
# print(a[1])

# dicte = {"cat": "Tom", "mouse": "Jerry"}
# dicte_1 = dict(cat="Tom", mouse="Jerry")
#
# for i in dicte:
#     print(dicte[i])
#
#
# for i in dicte.keys():
#     print(i)
#
# for i in dicte.values():
#     print(i)
#
# for i in dicte.items():
#     print(f"{i[0]} -> {i[1]}")
#
#
# liste = [1, 2, 3, 4, 5, 2, 4]
# #
# # for i in set(liste):
# #     print(i)
#
#
# print(liste[2:5])
# print(liste[:5])
# print(liste[2:])
# print(liste[::-1])


# def sum(a, b):
#     c = a + b
#     return c, a, b
#
# res = sum(1, 5)
# print(res)
#
# sum, a, b = sum(1, 5)
# print(sum, a, b)
#
# liste = [1, 2, 3]
# liste[0], liste[1] = liste[1], liste[0]
# print(liste)
#
# a, b = 1, 2

# a = input("Numbeer: ")
# try:
#     print(1/int(a))
# except ZeroDivisionError:
#     print("0")
# except ValueError:
#     print("LOX^2")
# except:
#     print("LOX")
# else:
#     print("Ощибочка")


# liste = [1, 3, 4, 5, 7]
#
# res = [i + 2 for i in liste]
# print(res)
#
# dicte = {"cat": "Tom", "mouse": "Jerry"}
# res = [i for i in dicte.values()].sort()
# print(res)
#
# res = []
# for i in dicte.values():
#     res.append(i)
#
# res = [i for i in dicte.values()]


# b = lambda a: a + 5
# print(b(1))
#
# liste = [1, 3, 4, 5, 7]
# # liste = list(map(str, liste))
# # print(liste)
#
# res = list(map(lambda c: c**3, liste))
# print(res)
#
# res = list(filter(lambda a: a < 4, liste))
# print(res)

# def sum(*a):
#     sum = 0
#     for i in a:
#         sum += i
#     return sum
#
# print(sum(1))
# print(sum(1, 2))
# print(sum(1, 2, 3))
# print(sum(1, 2, 3, 4))
#
# def timzone(time, tz):
#     print(time, tz)
#
# def convert_timefone(time, **kwargs):
#
#     return timzone(time, **kwargs)
#
# time = convert_timefone("time", tz="UK")

# liste = [1]
# listee = [2, 3, 4, 5]
#
# liste = [*liste, *listee]
#
# print(liste)


# f = open("text.txt", "r")
# text = f.read()
# f.close()
#
# from json import loads
#
# res = loads(text)
#
# res["order"]["status"] = "XREN'"
#
# f = open("text.txt", "w")
# text = f.write(str(res))
# f.close()


# class MyClass():
#     _name = "Dima"
#     _age = 12
#     __fasfd = 12
#
#
#     def __my(self):
#         print(f"Hello {self._name}")
#
#
# f = MyClass()
#
# f._MyClass__my()


# class MyClass():
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     def fefe(self):
#         print(self.name, self.age)
#
#
# dima = MyClass("Dima", 23)
# dima.fefe()

# class Rectangle(object):
#     def __init__(self, min_x, min_y, max_x, max_y):
#         self.min_x = min_x
#         self.min_y = min_y
#         self.max_x = max_x
#         self.max_y = max_y
#
#     def __eq__(self, other):
#         return (self.min_x == other.min_x and
#                 self.min_y == other.min_y and
#                 self.max_x == other.max_x and
#                 self.max_y == other.max_y)
#
# foo = Rectangle(0, 0, 42, 42)
# bar = Rectangle(4, 8, 15, 16)
#
# print(foo == bar) # всё ещё False
#
# baz = Rectangle(0, 0, 42, 42)
# print(foo == baz) # True
#
# print(foo == 10) # False

# from multipledispatch import dispatch
#
# class MyClacc():
#     @dispatch(str)
#     def my(self, a):
#         print(a)
#
#     @dispatch(str, str)
#     def my(self, a, b):
#         print(a, b)
#
# dima = MyClacc()
# dima.my("efw")
# dima.my("rrr", "rer")