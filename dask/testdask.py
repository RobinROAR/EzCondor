#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calcov
import os
try:
    import Image
except ImportError:
    from PIL import Image
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
    client = Client(args.address)
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
    result = [[np.array(_[0]),str(_[1]),str(_[2])] for _ in client.gather(future)]

    if os.path.exists(r'./data'):
        os.rmdir(r'./data')
    else:
        os.mkdir(r'./data')
    i = 0
    for _ in result:
        data=_[0]
        time=_[1]
        name = _[2].strip('tcp://')
        new_im = Image.fromarray(data)
        new_im.save('./data/result_%s_%s_(%s).jpg' % (i,time,name))
        i += 1


if __name__ == '__main__':

    parser = argparse.ArgumentParser(usage='./testdask.py --help')
    parser.add_argument('queue', type=int, nargs='?', default=1, help='the subtask you want')
    parser.add_argument('address', type=str, nargs='?', default='127.0.0.1:8786', help='scheduler address')
    args = parser.parse_args()
    main(None)


