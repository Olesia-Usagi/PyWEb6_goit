from multiprocessing import Process, Manager
from datetime import datetime


def factorize(name, number, fin):
    rezult = []
    for i in range(1, number+1):
        if number % i == 0:
            rezult.append(i)
    fin[name] = rezult


a, b, c, d = 128, 255, 99999, 10651060


if __name__ == '__main__':
    start_ = datetime.now()
    manager = Manager()
    mgr = manager.dict()
    Proc1 = Process(target=factorize, args=('a', a, m))
    Proc2 = Process(target=factorize, args=('b', b, m))
    Proc3 = Process(target=factorize, args=('c', c, m))
    Proc4 = Process(target=factorize, args=('d', d, m))

    Proc1.start()
    Proc2.start()
    Proc3.start()
    Proc4.start()

    Proc1.join()
    Proc2.join()
    Proc3.join()
    Proc4.join()

    print(mgr)

    end_ = datetime.now()
    print((end_ - start_).total_seconds())
