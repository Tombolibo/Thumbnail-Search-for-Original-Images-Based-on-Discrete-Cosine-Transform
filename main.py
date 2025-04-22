import os
import time

import numpy as np
import cv2



# 需求更变：
# 1. 需要总体数据数据库路径（所有的大图片）作为类初始化
# 2. 可以读入一张缩略图
# 3. 根据这个缩略图在总体数据库种找到最相似的前k张图片（可以调整相关阈值）
class SearchP2P(object):
    def __init__(self, dataBasePath, k = 20):
        self._dataBasePath = dataBasePath  # 原始图库（大图）路径
        self._files = np.array(os.listdir(self._dataBasePath), dtype=str)
        self._imgsDCT = np.zeros((len(self._files), 256), dtype=np.int8)  # 原图离散余弦变换的结果

        self._img = None  # 读取的缩略图
        self._imgDiscos = None  # 缩略图离散余弦变换的结果

        self._k = k  # 相似阈值
        self._indexs = []  # 寻找到的原图下标

        # 判断是否有缓存
        try:
            self._imgsDCT = np.load(self._dataBasePath+'.npy')
        except:
            for i,file in enumerate(self._files):
                suffix = os.path.splitext(file)[-1]
                if suffix == '.jpg' or suffix == '.png' or suffix == '.jepg':
                    imgTemp = cv2.imread(os.path.join(self._dataBasePath, file))
                    self._imgsDCT[i,:] = self.analysisImg(imgTemp)
            # 简单缓存到本地
            np.save(self._dataBasePath, self._imgsDCT)
            print(self._dataBasePath, 'saved!')
        else:
            print(self._dataBasePath, 'existed!')

    # 解析一张图片进行DCT转换，最后提取DCT左上8*8计算均值并返回哈希值
    def analysisImg(self, img):
        imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        DCT = cv2.dct(imgGray.astype(np.float32))  # 离散余弦变换
        DCTtl = DCT[:16, :16]  # 取左上角16*16共64个低频系数
        DCTtlBinary = (DCTtl > np.mean(DCTtl)).astype(np.int8)
        return DCTtlBinary.flatten()

    # 设置阈值
    def setK(self, k):
        self._k = k


    # 读取缩略图并寻找
    def readAndFind(self, imgPath):
        '''

        :param imgPath:   缩略图图像路径
        :return:   (原图文件下标、原图文件名称)
        '''
        self._img = cv2.imread(imgPath)
        if self._img is not None:
            self._imgDiscos = self.analysisImg(self._img)
            self.searchOrgimg()
        return self._indexs, self._files[self._indexs]

    # 在数据库中比较离散余弦变换的汉明距离，找到原图
    def searchOrgimg(self):
        result = np.sum(np.bitwise_xor(self._imgDiscos, self._imgsDCT), axis = 1)
        self._indexs = np.where(result<self._k)[0]  # 如果没有返回的为空arra





if __name__ == '__main__':

    # 初始化并设置原图库
    t1 = time.time()
    searcher = SearchP2P(r'./fruit', k=20)
    print('初始化时间：', 1000*(time.time()-t1), 'ms')

    path = r'./small'
    files = os.listdir(path)
    for file in files:


        # 读取缩略图
        t1 = time.time()
        result, fileName = searcher.readAndFind(os.path.join(path,file))
        print('查找时间：', 1000*(time.time()-t1), 'ms')
        print('原图文件名：', fileName)

        # =================展示结果===================
        print('result: ', result)
        print('缩略图大小：', searcher._img.shape)

        cv2.namedWindow('thumbnail', cv2.WINDOW_NORMAL)
        cv2.imshow('thumbnail', searcher._img)
        for i in result:
            imgOrg = cv2.imread(os.path.join(searcher._dataBasePath, searcher._files[i]))
            print('{}号原图大小：'.format(i), imgOrg.shape)
            cv2.namedWindow('img{}'.format(i), cv2.WINDOW_NORMAL)
            cv2.imshow('img{}'.format(i), imgOrg)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print('---------------------------------------------')


