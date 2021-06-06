# -*- coding: UTF-8 -*-
__author__ = 'Kay Zhou'

import time


def exeTime(func):
    def newFunc(*args, **args2):
        t0 = time.time()
        print("@ %s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__))
        back = func(*args, **args2)
        print("@ %s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__))
        print("@ %.3fs taken for {%s}" % (time.time() - t0, func.__name__))
        return back
    return newFunc


@exeTime
def test():
    _sum = 1
    for i in range(1, 10000):
        _sum *= i
    print(_sum)


if __name__ == '__main__':
    test()



