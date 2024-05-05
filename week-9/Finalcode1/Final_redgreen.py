import cv2
import numpy as np

def detect_colored(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 转换图像到HSV颜色空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 定义红色和绿色的HSV范围
    lower_red = np.array([152, 127, 25])  
    upper_red = np.array([179, 193, 255])  
    lower_green = np.array([48, 82, 39])  
    upper_green = np.array([121, 247, 255]) 

    # 根据颜色范围创建掩膜
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # 使用形态学操作对掩膜进行处理，去除噪音
    kernel = np.ones((5,5),np.uint8)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)

    # 在原始图像中找到红色和绿色光点的轮廓
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历轮廓并获取其外接圆
    for contour in contours_red:
        (x,y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(image, center, radius, (0,0,255), 2) # 在原图中画出红色圆点
        cv2.putText(image, f"({center[0]}, {center[1]})", (center[0]+10, center[1]+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    for contour in contours_green:
        (x,y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(image, center, radius, (0,255,0), 2) # 在原图中画出绿色圆点
        cv2.putText(image, f"({center[0]}, {center[1]})", (center[0]+10, center[1]+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image

if __name__ == "__main__":
    result_image = detect_colored('/home/xyq/vision/week-9/insrc/a.jpeg')
    cv2.namedWindow('Detected', cv2.WINDOW_NORMAL)
    cv2.imshow('Detected', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()