from PIL import Image
import cv2
import numpy as np


# w = 2048 * 2
# h = 1534 * 2
# focal_x = 0.5916212201869601 * w
# focal_y = 0.5916212201869601 * h
# c_x = 0.005470156959609551 * w
# c_y = -0.0005023180427906736 * h
# k1 = 0.04092749837698557
# k2 = -0.15340728768995107
# p1 = 0.00033011864688312466
# p2 = -0.00026447839524189847
# k3 = 0.06065589538631147

width =4056
height =3040
focal_x =0.5519586077506591 * width
focal_y =0.5519586077506591 * height
c_x =0.004708790244421668 * width
c_y =-0.0013531735497823493 * height
c_x = width/2
c_y = height/2
c_x = width/2 + 0.004708790244421668 * width / (6.1/1000)
c_y = height/2 + -0.0013531735497823493 * height / (4.7/1000)
k1 =0.13005528252728377
k2 =-0.18586482149919778
p1 =-0.0008843440868090323
p2 =0.0010300111848347369
k3 =0.07194021249125297

# image = Image.open('./photos/photo7.JPG')
mtx = np.array([
  (focal_x, 0, c_x),
  (0, focal_y, c_y),
  (0, 0, 1)
])
dist = np.array([k1, k2, p1, p2, k3])

img = cv2.imread('./photos/photo7.JPG') 
# scaled_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(
#     mtx, dist, img.shape[0:2], 1, img.shape[0:2]
# )

dst = cv2.undistort(img, mtx, dist, None, mtx)
# roi_x, roi_y, roi_w, roi_h = roi
# cropped_frame = dst[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]

cv2.imwrite('./results/result.jpg', dst)

# Image.fromarray(dst).save('results/result.png')
