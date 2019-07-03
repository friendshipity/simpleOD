# simpleOD
simple  
大图
![image](https://github.com/yyq90/simpleOD/blob/master/images/test.jpg)


使用的方法  
相似度的衡量
根据小图T的尺寸，通过滑动窗口检测大图切片I(x+x',y+y')(下面用I'表示)，针对小图所有x',y',检测其和T(x‘,y’)是否都相等。


相似度
#### 1.array match  
result：
缺点，只是检测到和小图像素值完全一样的区域。
#### 2.template match  
类似1,计算T和I'
是cv2.matchTemplate(imageGray,boxGray,cv2.TM_CCOEFF)的具体实现。
缺点，仍然为template matching，泛化能力低，只能取图中与小图相同的框。但是相较于方法1，允许template像素值于I'的不同
#### 3.pixal iou
如果需要检测相同颜色的飞机。可以给I'和T设定阈值，保留阈值以上形成mask,在计算所有通道mask I'和mask T的iou值。

#### 4.ssim  
类似1，计算T和I'的ssim(structural similarity)Index，亮度、对比度和结构

ssim效果较好。
得到每个滑动窗口的得分后，取score排序top200的框.用score,坐标的x,y三个feature进行kmeans聚类（ssim的score,小于1，可以放大score，这样可以加强score feature的权重）。
取score mean最高的类中的box作为最后的输出。

讨论:  
1. 在此任务中，使用聚类这种方法可能会导致的泛化能力的降低(比如需要检测不同动作和颜色的所有飞机)。这个时候可以考虑使用nms对score top100个框进行处理。
2. 不同于直接计算T和I'的相似度，可以用hog，orb方法提取feature进行比较或者训练。
