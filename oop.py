class SomeClass(object):
    attr1 = 42

    def method1(self, x):
        return 2*x

obj = SomeClass()
print(obj.method1(6)) # 12
print(obj.attr1) # 42


# -----------------------------------------------------------------

class Point(object):
    def __init__(self, x, y, z):
        self.coord = (x, y, z)

p = Point(13, 14, 15)
print(p.coord) # (13, 14, 15)

# -----------------------------------------------------------------

class SomeClass(object):
    pass

def squareMethod(self, x):
    return x*x

SomeClass.square = squareMethod
obj = SomeClass()
print(obj.square(5)) # 25

# -----------------------------------------------------------------

class SomeClass(object):
    @staticmethod
    def hello():
        print("Hello, world")

print(SomeClass.hello()) # Hello, world
obj = SomeClass()
print(obj.hello()) # Hello, world

# -----------------------------------------------------------------

class SomeClass(object):
    def __init__(self, name):
        self.name = name

    def __del__(self):
        print('удаляется объект {} класса SomeClass'.format(self.name))

obj = SomeClass("John");
del obj # удаляется объект John класса SomeClass