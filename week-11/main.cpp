#include <opencv2/opencv.hpp>
#include <iostream>

class ColorDetector {
public:
    ColorDetector(const std::string& imagePath) : image(cv::imread(imagePath)) {}

    cv::Mat detectColored() {
        //Color detection logic
        // 转换图像到HSV颜色空间
        cv::Mat hsv;
        cv::cvtColor(image, hsv, cv::COLOR_BGR2HSV);

        // 定义红色和绿色的HSV范围
        cv::Scalar lower_red(152, 127, 25);
        cv::Scalar upper_red(179, 193, 255);
        cv::Scalar lower_green(48, 82, 39);
        cv::Scalar upper_green(121, 247, 255);

        // 根据颜色范围创建掩膜
        cv::Mat mask_red, mask_green;
        cv::inRange(hsv, lower_red, upper_red, mask_red);
        cv::inRange(hsv, lower_green, upper_green, mask_green);

        // 使用形态学操作对掩膜进行处理，去除噪音
        cv::Mat kernel = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(5, 5));
        cv::morphologyEx(mask_red, mask_red, cv::MORPH_OPEN, kernel);
        cv::morphologyEx(mask_green, mask_green, cv::MORPH_OPEN, kernel);

        // 在原始图像中找到红色和绿色光点的轮廓
        std::vector<std::vector<cv::Point>> contours_red, contours_green;
        cv::findContours(mask_red, contours_red, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);
        cv::findContours(mask_green, contours_green, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE);

        // 遍历轮廓并获取其外接圆
        for (const auto& contour : contours_red) {
            cv::Point2f center;
            float radius;
            cv::minEnclosingCircle(contour, center, radius);
            cv::circle(image, center, static_cast<int>(radius), cv::Scalar(0, 0, 255), 2); // 在原图中画出红色圆点
            cv::putText(image, "(" + std::to_string(static_cast<int>(center.x)) + ", " + std::to_string(static_cast<int>(center.y)) + ")",
                        cv::Point(static_cast<int>(center.x) + 10, static_cast<int>(center.y) + 10), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 0, 255), 2);
        }

        for (const auto& contour : contours_green) {
            cv::Point2f center;
            float radius;
            cv::minEnclosingCircle(contour, center, radius);
            cv::circle(image, center, static_cast<int>(radius), cv::Scalar(0, 255, 0), 2); // 在原图中画出绿色圆点
            cv::putText(image, "(" + std::to_string(static_cast<int>(center.x)) + ", " + std::to_string(static_cast<int>(center.y)) + ")",
                        cv::Point(static_cast<int>(center.x) + 10, static_cast<int>(center.y) + 10), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 255, 0), 2);
        }

        return image;
 

    }

private:
    cv::Mat image;
};

class RectangleDetector {
public:
    cv::Mat detectRectangles(const std::string& imagePath) {
        // Rectangle detection logic
        //         // 你之前的 detectRectangles 函数代码
        cv::Mat image = cv::imread(imagePath);

    // 转换为灰度图像并进行高斯模糊
    cv::Mat gray, blurred;
    cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
    cv::GaussianBlur(gray, blurred, cv::Size(5, 5), 0);

    // 应用Canny边缘检测
    cv::Mat edges;
    cv::Canny(blurred, edges, 50, 150);

    // 查找轮廓
    std::vector<std::vector<cv::Point>> contours;
    std::vector<cv::Vec4i> hierarchy;
    cv::findContours(edges, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_SIMPLE);

    // 初始化一个列表来存储所有检测到的矩形角点
    std::vector<std::vector<cv::Point>> detectedRectanglesCorners;

    // 遍历所有轮廓
    for (const auto& contour : contours) {
        // 近似轮廓
        double epsilon = 0.03 * cv::arcLength(contour, true);
        std::vector<cv::Point> approx;
        cv::approxPolyDP(contour, approx, epsilon, true);

        // 检查轮廓是否有4个顶点
        if (approx.size() == 4) {
            // 计算轮廓的边界框
            cv::Rect boundingRect = cv::boundingRect(approx);
            float aspectRatio = static_cast<float>(boundingRect.width) / boundingRect.height;

            // 根据需要设置长宽比阈值来过滤掉非矩形轮廓
            if (0.3 < aspectRatio && aspectRatio < 1.5) {
                // 获取四个角点
                std::vector<cv::Point> corners = approx;

                // 判断当前检测到的矩形角点是否与之前的角点太接近
                bool tooClose = false;
                for (const auto& prevCorners : detectedRectanglesCorners) {
                    for (const auto& corner : corners) {
                        for (const auto& prevCorner : prevCorners) {
                            if (std::abs(corner.x - prevCorner.x) < 10 && std::abs(corner.y - prevCorner.y) < 10) {
                                tooClose = true;
                                break;
                            }
                        }
                        if (tooClose) break;
                    }
                    if (tooClose) break;
                }

                if (!tooClose) {
                    detectedRectanglesCorners.push_back(corners);

                    // 绘制轮廓和角点
                    cv::drawContours(image, std::vector<std::vector<cv::Point>>{approx}, -1, cv::Scalar(0, 255, 0), 2);
                    for (const auto& corner : corners) {
                        cv::circle(image, corner, 5, cv::Scalar(255, 0, 0), -1);
                        int textX = corner.x + 5 < image.cols - 10 ? corner.x + 5 : corner.x - 45;
                        int textY = corner.y - 5 > 10 ? corner.y - 5 : corner.y + 25;

                        cv::putText(image, "(" + std::to_string(corner.x) + ", " + std::to_string(corner.y) + ")", 
                                    cv::Point(textX, textY), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(255, 100, 0), 2);
                    }
                }
            }
        }
    }

    // 如果检测到了至少一个矩形
    if (!detectedRectanglesCorners.empty()) {
        // 获取最后一个矩形的四个角点
        std::vector<cv::Point> corners = detectedRectanglesCorners.back();

        // 获取矩形边界框
        cv::Rect rect = cv::boundingRect(corners);

        // 计算矩形中心坐标
        int rectCenterX = rect.x + rect.width / 2;
        int rectCenterY = rect.y + rect.height / 2;

        // 绘制矩形中心坐标
        cv::circle(image, cv::Point(rectCenterX, rectCenterY), 5, cv::Scalar(0, 0, 255), -1);
        cv::putText(image, "(" + std::to_string(rectCenterX) + ", " + std::to_string(rectCenterY) + ")", 
                    cv::Point(rectCenterX + 10, rectCenterY - 10), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 150, 255), 2);
    }
        return image;

    }
};

int main() {
    std::string image_path = "a.jpeg";

    ColorDetector colorDetector(image_path);
    cv::Mat redGreenImage = colorDetector.detectColored();

    RectangleDetector rectangleDetector;
    cv::Mat cornerImage = rectangleDetector.detectRectangles(image_path);

    cv::Mat finalImage;
    cv::addWeighted(cornerImage, 0.5, redGreenImage, 0.5, 0, finalImage);

    cv::namedWindow("Final Image", cv::WINDOW_NORMAL);
    cv::imshow("Final Image", finalImage);
    cv::waitKey(0);
    cv::destroyAllWindows();

    return 0;
}