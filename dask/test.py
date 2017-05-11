import os

import dask.array as da
import numpy as np

A = da.ones((500,500,500), chunks=(100, 100,100))

print np.array(A).shape