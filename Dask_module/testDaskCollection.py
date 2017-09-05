#!/usr/bin/env python
# -*- coding: utf-8 -*-

import calcov
import os
import time
from PIL import Image
import numpy as np
from distributed import Client
import distributed
import dask.array as da
import dask
import argparse
import shutil



def cal(x,client):
    st = time.time()

    #Distributed scheduler
    #with dask.set_options(get=dask.threaded.get):
    with dask.set_options(get=client.get):
        A = da.transpose(x)
        B = da.dot(x,A)
        C = da.dot(B,B)

        print C.compute()

    #Default scheduler
    # with dask.set_options(get=dask.threaded.get):
    #     A = da.transpose(x)
    #     B = da.dot(x,A)
    #     C = da.dot(B,B)
    #
    #     print C.compute()

    #mannually set global thread.
    # from multiprocessing.pool import ThreadPool
    # with dask.set_options(pool=ThreadPool(4)):
    #     A = da.transpose(x)
    #     B = da.dot(x,A)
    #     C = da.dot(B,B)
    #
    #     print C.compute(num_works = 4)




    print 'time: ',time.time()-st
    return 0

def main():
    #Generate scheduler
    #print np.array(Image.open(r'dota2.jpg')).shape

    #data = da.from_array(np.array(Image.open(r'dota2.jpg')), chunks=(40,60,3))
    data = da.from_array(np.ones((800,600)), chunks=(800,600))

    client = Client('127.0.0.1:8786')
    #client = 0
    cal(data,client)



if __name__ == '__main__':
    main()



