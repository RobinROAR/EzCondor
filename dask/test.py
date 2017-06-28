#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calcov
import os
import Image
import numpy as np
from distributed import Client
import distributed
import dask.array as da
import argparse
import time


def cal(x):
    worker = distributed.get_worker()  # The worker on which this task is running
    print worker.data.fast
    print worker.address
    # print time.asctime(time.localtime(time.time()))
    #print int(x.min()+x.max())
    return x.sum()




def main(_):
    #Generate scheduler
    data = da.from_array(np.array(Image.open(r'dota2.jpg')), chunks=(600, 400, 3))
    client = Client(_)
    #client.upload_file('calcov.py')

    temp3 = np.zeros((3, 3))
    temp3[0, :] = [0.062467, 0.125000, 0.062467]
    temp3[1, :] = [0.125000, 0.250131, 0.125000]
    temp3[2, :] = [0.062467, 0.125000, 0.062467]




    future = client.compute(cal(data))
    #print future.result()
    print client.gather(future)
    result = int(client.gather(future))

    print result
if __name__ == '__main__':

    main('127.0.0.1:8786')


