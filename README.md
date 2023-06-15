# FaceDet

This is a face detection python binding module,
the face detection model and face detection code is from
<https://github.com/ShiqiYu/libfacedetection>

## install

clone the repo

```base
git clone https://github.com/iYuqinL/facedet.git
```

install the python pakage

```bash
# go to the facedet directory
python3 setup.py install
```

## usage

after install the python package, just

```python
import os
import cv2
import numpy as np
import pyfacedet as facedet

imgpath = "~/Pictures/test.jpeg"
imgpath = os.path.expanduser(imgpath) 
imarr = cv2.imread(imgpath)
print(isinstance(imarr, np.ndarray))
print(imarr.shape, imarr.dtype)
res = facedet.detect_face(imarr)
print(res)
```
