#!/usr/bin/env python
def a_sum(x,y):
    return x + y

x = int(raw_input("First Integer: "))
y = int(raw_input("Second Integer: "))
z = a_sum(x,y)
print "Sum of {0} and {1} is: {2}".format(x, y, z)
