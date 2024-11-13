import cProfile


def my_function():
    a = 0
    for i in range(1, 10000000):
        a += i
    print(a)


cProfile.run('my_function()')
