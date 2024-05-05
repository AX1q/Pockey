import cv2
import numpy as np

def detect_rectangles(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 转换为灰度图像并进行高斯模糊
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 应用Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 初始化一个列表来存储所有检测到的矩形角点
    detected_rectangles_corners = []

    # 遍历所有轮廓
    for contour in contours:
        # 近似轮廓
        epsilon = 0.03 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # 检查轮廓是否有4个顶点
        if len(approx) == 4:
            # 计算轮廓的边界框
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h

            # 根据需要设置长宽比阈值来过滤掉非矩形轮廓
            if 0.3 < aspect_ratio < 1.5:
                # 获取四个角点
                corners = np.squeeze(approx)  # 直接获取角点数组
                detected_rectangles_corners.append(corners)

                # 绘制轮廓和角点
                cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
                for corner in corners:
                    x, y = corner
                    cv2.circle(image, (x, y), 5, (255, 0, 0), -1)
                    text_x = x + 5 if x + 5 < image.shape[1] - 10 else x - 5
                    text_y = y - 5 if y - 5 > 10 else y + 5
                    cv2.putText(image, f"({x}, {y})", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
                
                # 遍历所有检测到的矩形角点
                for corners in detected_rectangles_corners:
                    # 获取矩形边界框
                    rect_x, rect_y, rect_w, rect_h = cv2.boundingRect(corners)

                    # 计算矩形中心坐标
                    rect_center_x = rect_x + rect_w // 2
                    rect_center_y = rect_y + rect_h // 2

                    # 绘制矩形中心坐标
                    cv2.circle(image, (rect_center_x, rect_center_y), 5, (0, 0, 255), -1)
                    cv2.putText(image, f"({rect_center_x}, {rect_center_y})", (rect_center_x + 10, rect_center_y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    return image

if __name__ == "__main__":
    result_image = detect_rectangles('a.jpeg')
    cv2.namedWindow('Detected', cv2.WINDOW_NORMAL)
    cv2.imshow('Detected', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()