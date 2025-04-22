# Thumbnail-Search-for-Original-Images-Based-on-Discrete-Cosine-Transform
基于离散余弦变换的缩略图到原图搜索

## 以原图数据库以及识别阈值创建实列
检测到新的原图数据库会生成该原图数据库的离散余弦变换低频信息二值化后的矩阵并保存(默认左上角16*16)低频信息<br/>
设置好原图数据库后使用readAndFind(缩略图路径）查找，如果缩略图和原图DCT低频二值化汉明距离小于K值，认为找到原图<br/>
阈值K可以通过类实例设定

