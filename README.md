# simpleOD
  
测试大图  
test.jpg  
  
![image](https://github.com/yyq90/simpleOD/blob/master/images/test.jpg)  
  
测试小图  
  
![image](https://github.com/yyq90/simpleOD/blob/master/images/crop.png)    
crop.png  

![image](https://github.com/yyq90/simpleOD/blob/master/images/crop2.png)      
crop2.png  
使用的方法  
滑动窗口，相似度,聚类



## 相似度  
根据小图T的尺寸，通过滑动窗口检测大图切片I(x+x',y+y')(I')，针对小图所有x',y'，检测其和T(x‘,y’)的相似度 。   
#### 1.pixel match  
计算T和I'是否完全一致
result:  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_raw_crop_2.png)    
crop.png  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_raw_crop2.png)    
crop2.png  

缺点，只是检测到和小图像素值完全一致的区域。
#### 2. cross coefficient 
计算T和I'的cross coefficient，是cv2.matchTemplate(imageGray,boxGray,cv2.TM_CCOEFF)的具体实现。  
result:  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_ccoeff2.png)    
crop.png  cluster_num=2  top_n=200  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_ccoeff3.png)    
crop.png  cluster_num=3  top_n=200  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_ccoeff_crop2_5.png)    
crop2.png  cluster_num=5  top_n=200  

缺点，仍然为template matching，泛化能力低，只能取图中与小图相同的框。但是相较于方法1，允许T像素值于I'的不同。    

#### 3.pixal iou
如果需要检测对颜色不敏感。可以给I'和T设定阈值，保留阈值以上形成mask,计算所有通道mask I'和mask T的iou值。  
result:  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_iou_crop_2.png)    
crop.png  cluster_num=2  top_n=200  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_iou_crop_3.png)    
crop.png  cluster_num=3  top_n=200  
 
缺点，由于设定阈值，丢失了一些细节和结构信息，检出率稍高，但容易误检  

#### 4.ssim  
计算T和I'的ssim(structural similarity)Index  
result:  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_ssim_crop_2.png)    
crop.png  cluster_num=2  top_n=200  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_ssim_crop_3.png)    
crop.png  cluster_num=3  top_n=200  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_ssim_crop_4.png)    
crop.png  cluster_num=4  top_n=200  
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_ssim_crop_5.png)    
crop.png  cluster_num=5  top_n=200     
![image](https://github.com/yyq90/simpleOD/blob/master/images/det_ssim_crop2_5.png)    
crop2.png  cluster_num=5  top_n=200  

得出的候选区域比较靠谱(得分和图谱相似度的线性度较高)，从亮度，对比度和结构衡量图片的相似度。  
缺点,计算较慢，候选区域较多，top_n的值需要调大在测试。但是这样也增加了后面kmeans的计算量  
## 聚类  

得到每个滑动窗口的得分后，取score排序top200的框。用score，坐标的x，y，三个feature进行kmeans聚类（ssim的score小于1，可以放大score，这样可以加强score feature的权重）。
取score mean最高的类中的box作为最后的输出。类别数量num_cluster 和 top_n 作为超参。

## 讨论:  
1. 在此任务中，使用聚类这种方法可能会导致的泛化能力的降低(比如需要检测不同动作和颜色的所有飞机)。这个时候可以考虑使用nms对score top100个框进行处理。
2. 不同于直接计算T和I'的相似度，可以用hog，orb方法提取feature进行比较或者训练。
3. 可以在大图上采样neg sample，和一张pos sample的加噪, 用siamese网络去训练。
