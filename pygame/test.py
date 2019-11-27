import random

a = [random.randint(0, 5) for i in range(10)]
print(a)
a[5] = -1
a[6] = -1
a[7] = -1
print(a)
for i in range(len(a)):
    pass