#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    import Image
except ImportError:
    from PIL import Image
import time
import dask
import numpy as np
import distributed

# 通过原始定义的方法，对图像计算卷积，返回一个图像矩阵。
# calculate the convolution by brute force, return a image matrix.
def getTemSize(temp):
    wid = temp.shape[0]
    print '++++++++++++++++++++++++++++++++'
    print "COV template:"
    print temp
    print 'Template size:', wid, '*', wid
    return wid


def calCov(tem,img):
    st = time.time()
    print 'Input image : ', img.shape

    size = getTemSize(tem)
    # 扩充图片的像素数
    es = (size - 1) / 2

    # 区别灰度图像与彩色图像
    if len(img.shape) is 2:
        y, x, z = img.shape[0], img.shape[1], 1
    else:
        y, x, z = img.shape[0], img.shape[1], img.shape[2]
    # 将图像上下左右各增加（模板宽度-1)/2个像素，用于计算卷积时的边界计算。
    # Expand image by es pixel around for edge calculation.
    if len(img.shape) is 2:
        eimg = np.uint8(np.zeros((y + 2 * es, x + 2 * es, 1)))
        eimg[es:y + es, es:x + es, 0] = img[:, :]
    else:
        eimg = np.uint8(np.zeros((y + 2 * es, x + 2 * es, z)))
        eimg[es:y + es, es:x + es, :] = img

    result = np.uint8(np.zeros(eimg.shape))
    x = x + es
    y = y + es
    for i in range(z):
        a = b = 1
        # 扩充后图像的坐标,从0开始
        # 设置一个dif变量，用于卷积窗内计算。
        dif = (size - 1) / 2
        while (b < y):
            a = 1
            while (a < x):
                cntx = 0
                dify = size / 2
                result[b][a][i] = 0
                while (cntx < size):
                    cnty = 0
                    difx = size / 2
                    while (cnty < size):
                        # print b,a,b-dify,a-difx
                        result[b][a][i] += tem[cntx][cnty] * eimg[b - dify][a - difx][i]
                        cnty += 1
                        difx -= 1
                    cntx += 1
                    dify -= 1
                a += 1
            b += 1
    et = time.time()
    print 'Cal time:', str(et - st)
    work = distributed.get_worker()
    return [result,str(et - st),work.address]
