#!/usr/bin/env python

def some_func():
    print "inside some_func"
def some_func2():
    print "inside some_func2"

def main_exec():
    print "Hello"
    some_func2()

if __name__ == "__main__":
    main_exec()
