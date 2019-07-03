import numpy as np
import cv2
import sys
from skimage.measure import compare_ssim as ssim


def raw_method(img, template):
    A = img == template
    return A.all()


def cross_coefficient(img, template):
    imgGrey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    templateGrey = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    return ((imgGrey - imgGrey.mean()) * (templateGrey - templateGrey.mean())).sum()


def pixel_threshold_iou(img, template, p=0.3):
    img = img.astype(np.float32) / 255
    template = template.astype(np.float32) / 255
    img[img < p] = 0
    template[template < p] = 0

    ious = []
    for i in range(3):
        intersection = np.logical_and(img[i], template[i]).sum()
        union = np.logical_or(img[i], template[i]).sum()
        if union != 0:
            ious.append(intersection / union)
    return np.array(ious).mean()


def SSIM(img, template):
    return ssim(img, template, multichannel=True)


positions = []
img = cv2.imread(sys.argv[1])
box = cv2.imread(sys.argv[2])

X, Y, _ = np.shape(img)
bx, by, _ = np.shape(box)
for i in range(0, X - bx, 1):
    for j in range(0, Y - by, 1):
        positions.append((raw_method(img[i:i + bx, j:j + by, :], box) + 0, i, j))
sorted = sorted(positions, key=lambda k: k[0])[-200:]

from sklearn.cluster import KMeans

cluster_num = 2

kmeans = KMeans(n_clusters=cluster_num)
w = np.array(sorted)
w[:, 0] = w[:, 0] * 1000
y = kmeans.fit(w)
pred = np.hstack((y.labels_.reshape(200, 1), np.array(sorted)))

max_mean = 0
max_index = None
for l in range(cluster_num):
    mean = pred[pred[:, 0] == l][:, 1].mean()
    if mean > max_mean:
        max_mean = mean
        max_index = l
results=[]
for v in pred[pred[:, 0] == max_index]:
    # cv2.rectangle(img, (int(v[3]), int(v[2])), (int(v[3]) + by, int(v[2]) + bx), (0, 255, 0), 1)
    results.append( (int(v[2]),int(v[3]), int(v[2]) + bx,int(v[3]) + by))
# cv2.imwrite('det_raw_crop_2.png', img)
print(results)

# font = cv2.FONT_HERSHEY_SIMPLEX
# for index,v in enumerate(sorted[-150:]):
#     if not v[0]>0:
#         continue
#     label = y_pred.labels_[index+50]
#     if label == 0:
#         cv2.rectangle(img, (v[2], v[1]), (v[2] + by, v[1] + bx), (255, 0, 0), 1)
#
#     elif label ==1:
#         cv2.rectangle(img, (v[2], v[1]), (v[2] + by, v[1] + bx), (0, 255, 0), 1)
#
#     elif label == 2:
#         cv2.rectangle(img, (v[2], v[1]), (v[2] + by, v[1] + bx), (0, 0, 255), 1)
#
#     elif label == 3:
#         cv2.rectangle(img, (v[2], v[1]), (v[2] + by, v[1] + bx), (255, 255, 0), 1)
#
#     elif label ==4 :
#         cv2.rectangle(img, (v[2], v[1]), (v[2] + by, v[1] + bx), (0, 255, 255), 1)
#
#     # cv2.putText(img, (v[2], v[1]), (v[2] + by, v[1] + bx), (255, 255, 255), 1)
#     cv2.putText(img, '%.2f' % v[0], (v[2], v[1]), font, 0.2, (0, 255, 0), 1)
# bbox.append((v[2],v[1],v[2]+by,v[1]+bx))
