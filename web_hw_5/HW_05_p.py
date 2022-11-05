from multiprocessing import Pool, current_process, cpu_count
from datetime import datetime


def factorize(number):
    rezult = []
    for i in range(1, number+1):
        if number % i == 0:
            rezult.append(i)
    return rezult


def callback(result):
    a, b, c, d = result
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == '__main__':
    start_ = datetime.now()
    with Pool(cpu_count()) as pross:
        pross.map_async(factorize, [128, 255, 99999, 10651060], callback=callback)
        pross.close()
        pross.join()

    end_ = datetime.now()
    print((end_ - start_).total_seconds())
