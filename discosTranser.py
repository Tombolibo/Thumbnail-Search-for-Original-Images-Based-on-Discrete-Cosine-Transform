import pickle

import numpy as np
import cv2



 # 解析一张图片进行DCT转换，最后提取DCT左上8*8计算均值并返回哈希值
def analysisImg(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    DCT = cv2.dct(imgGray.astype(np.float32))  # 离散余弦变换
    DCTtl = DCT[:16, :16]  # 取左上角8*8共64个低频系数
    DCTtlBinary = (DCTtl > np.mean(DCTtl)).astype(np.int32)
    print(DCTtlBinary.flatten().shape)
    return DCTtlBinary.flatten()


if __name__ == '__main__':
    imgS = cv2.imread(r'./small/apple1S.jpg')
    img = cv2.imread(r'./fruit/apple1.jpg')
    img = cv2.resize(img, None, None, 0.4, 0.8)
    cv2.imshow('img', img)
    cv2.waitKey(0)
    resultS = analysisImg(imgS)
    result = analysisImg(img)

    print(np.sum(cv2.bitwise_xor(resultS, result)))
