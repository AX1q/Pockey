import cv2 
import numpy as np
from Mycode_rec import detect_rectangles
from Mycode_Color import detect_colored

image_path = 'a.jpeg'
image = cv2.imread(image_path)

# 红绿点图像
RedGreen_image = detect_colored(image_path)

# 角点和中点坐标图像
corner_image = detect_rectangles(image_path)

# 图像叠加
Final_image = cv2.addWeighted(corner_image, 0.5, RedGreen_image, 0.5, 0)

# 显示结果
cv2.namedWindow('Final Image',cv2.WINDOW_NORMAL)
cv2.imshow('Final Image',Final_image)
cv2.waitKey(0)
cv2.destroyAllWindows()