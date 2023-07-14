class MyClass:
    color = "красный"

    def set(txt):
        MyClass.color = txt

    def show():
        print(MyClass.color)

MyClass.show()
MyClass.set("зелёный")
print(MyClass.color)

MyClass.color = "синий"
MyClass.show()

A = MyClass()
B = MyClass()

print("Class: ", MyClass.color)
print("A: ", A.color)
print("B: ", B.color)

A.color = "белый"

print("Class: ", MyClass.color)
print("A: ", A.color)
print("B: ", B.color)

MyClass.color = "жолтый"

print("Class: ", MyClass.color)
print("A: ", A.color)
print("B: ", B.color)

del A.color

print("Class: ", MyClass.color)
print("A: ", A.color)
print("B: ", B.color)
