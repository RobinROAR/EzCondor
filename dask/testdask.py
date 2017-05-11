#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calcov
import Image
import time
import dask
import numpy as np
from distributed import Client
import distributed
import dask.array as da
import argparse


# def cal(x):
#     worker = distributed.get_worker()  # The worker on which this task is running
#     print worker
#     print time.asctime(time.localtime(time.time()))
#     print int(x.min()+x.max())
#     return x.min()+x.max()


args = None

def main(_):
    #Generate scheduler
    data = da.from_array(np.array(Image.open(r'dota2.jpg')), chunks=(600, 400, 3))
    client = Client('127.0.0.1:8786')
    client.upload_file('calcov.py')

    temp3 = np.zeros((3, 3))
    temp3[0, :] = [0.062467, 0.125000, 0.062467]
    temp3[1, :] = [0.125000, 0.250131, 0.125000]
    temp3[2, :] = [0.062467, 0.125000, 0.062467]



    D = []
    B = []
    for i in range(args.queue):
        D.append(np.array(data + i * 10))
        B.append(temp3 + 0.05)

    future = client.map(calcov.calCov, B, D)
    result = [np.array(_) for _ in client.gather(future)]

    i = 0
    for _ in result:
        new_im = Image.fromarray(_)
        new_im.save('result_%s.jpg' % (i))
        i += 1


if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage='./testdask.py --help')
    parser.add_argument('queue', type=int, default=1, help='the subtask you want')
    args = parser.parse_args()
    main(None)


