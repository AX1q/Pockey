import cv2
import numpy as np

def detect_and_mark_quadrilaterals(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 消噪和增强
    denoised_image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    alpha = 1.0  # 对比度增强参数
    beta = 15  # 亮度增强参数
    enhanced_image = cv2.convertScaleAbs(denoised_image, alpha=alpha, beta=beta)

    # 边缘检测
    edges = cv2.Canny(enhanced_image, 50, 150)

    # 查找轮廓
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 标记四边形
    marked_image = image.copy()
    quadrilaterals = []
    for contour in contours:
        # 计算轮廓的面积
        area = cv2.contourArea(contour)

        # 排除面积较小的轮廓
        if area > 2000:
            # 计算轮廓的周长
            perimeter = cv2.arcLength(contour, True)

            # 对轮廓进行多边形逼近
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            # 如果逼近的轮廓是四边形，将其标记在图像上
            if len(approx) == 4:
                cv2.drawContours(marked_image, [approx], -1, (255, 0, 0), 2)
                quadrilaterals.append(approx)

                # 在图像上标出四边形的角点和中心位置，并显示坐标
                for point in approx:
                    cv2.circle(marked_image, tuple(point[0]), 5, (0, 0, 255), -1)  # 角点
                    cv2.putText(marked_image, f"({point[0][0]}, {point[0][1]})", (point[0][0] + 10, point[0][1] + 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 100, 100), 2)

                # 计算四边形的中心位置
                moments = cv2.moments(approx)
                cX = int(moments["m10"] / moments["m00"])
                cY = int(moments["m01"] / moments["m00"])
                cv2.circle(marked_image, (cX, cY), 5, (0, 150, 150), -1)  # 中心位置
                cv2.putText(marked_image, f"({cX}, {cY})", (cX + 10, cY + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 150, 150), 2)

    return marked_image

# 测试
if __name__ == "__main__":
    image_path = 'week-9/insrc/a.jpeg'
    marked_image = detect_and_mark_quadrilaterals(image_path)

    # 显示标记了四边形和角点的图像
    cv2.namedWindow("Marked Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Marked Image", marked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()