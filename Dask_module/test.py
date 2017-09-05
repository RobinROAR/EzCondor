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


class Apple:
    def __init__(self):
        self._age = 0

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self,value):
        if value !=0:
            self._size = value



a = [1, 2, 3, 4, 5]
b = [3, 4, 5,6]
if set(b).issubset(set(a)):
    print 1