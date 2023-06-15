# -*- coding:utf-8 -*-
###
# File: testfacedet.py
# Created Date: Wednesday, June 14th 2023, 11:19:38 pm
# Author: iYuqinL
# -----
# Last Modified: Thu Jun 15 2023
# Modified By: iYuqinL
# -----
# Copyright © 2023 iYuqinL Holding Limited
# 
# All shall be well and all shall be well and all manner of things shall be well.
# Nope...we're doomed!
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
###
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

imarr_res = imarr.copy()
for i in range(len(res)):
    face = res[i]
    score = face[0]
    x, y, w, h = face[1:5]
    
    cv2.putText(imarr_res, f"{score:02d}", (x, y-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(imarr_res, (x, y, w, h), (0, 255, 0), 2)
    cv2.circle(imarr_res, (face[5], face[5 + 1]), 1, (255, 0, 0), 2)
    cv2.circle(imarr_res, (face[5 + 2], face[5 + 3]), 1, (0, 0, 255), 2)
    cv2.circle(imarr_res, (face[5 + 4], face[5 + 5]), 1, (0, 255, 0), 2)
    cv2.circle(imarr_res, (face[5 + 6], face[5 + 7]), 1, (255, 0, 255), 2)
    cv2.circle(imarr_res, (face[5 + 8], face[5 + 9]), 1, (0, 255, 255), 2)

cv2.imwrite("result.png", imarr_res)