#!/usr/bin/env python


def func1():
    print "Hello World"


class MyClass(object):

    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password

    def hello(self):
        print "Welcome! IP is: {0}, user is {1}, passw is {2}".format(self.ip, self.user, self.password)

    def not_hello(self):
        print "Not Hello!!! IP is {0}, user is {1}, passw is {2}".format(self.ip, self.user, self.password)

class MyChildClass(MyClass):
    def __init__(self, ip, user, password, z=10):
        self.z = z
        MyClass.__init__(self, ip, user, password)
    def hello(self):
        print "Child welcome..IP is {0}".format(self.ip)




def main():
    func1()
    a = MyClass("1.1.1.1", "ali", "bdbdbdb")
    a.hello()
    a.not_hello()    
    b = MyChildClass("2.2.2.2", "veli", "ssss")
    b.hello()
    b.not_hello()
    print b.z

if __name__ == "__main__":
    main()
