import cv2  
import numpy as np  
  
# 读取图像  
image = cv2.imread('week-9/insrc/d.jpeg')  
new_width = 640  # 新宽度  
new_height = 490  # 新高度  
image = cv2.resize(image, (new_width, new_height)) 
# 获取调整尺寸后的图片的高度和宽度  
height, width = image.shape[:2]

# 转换为灰度图像  
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  

gray = cv2.GaussianBlur(gray,(9,9),3)
# 应用Canny边缘检测  
edges = cv2.Canny(gray, 50, 150)  
  
# 查找轮廓  
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
  
# 初始化一个列表来存储矩形的四个角坐标  
rectangles_corners = []

# 筛选和排序轮廓，找到最大的轮廓  
contours = sorted(contours, key=cv2.contourArea, reverse=True)  
for cnt in contours:  
    # 近似轮廓  
    epsilon = 0.02 * cv2.arcLength(cnt, True)  
    approx = cv2.approxPolyDP(cnt, epsilon, True)  
      
    # 如果轮廓有4个顶点，那么它可能是一个矩形  
    if len(approx) == 4:  
        # 获取四个角点  
        corners = approx.reshape((-1, 2))    
        rectangles_corners.append(corners)

# 设置坐标轴的颜色、线宽等参数  
axis_color = (255, 0, 0)  # BGR格式，蓝色  
tick_color = (0, 255, 0)  # BGR格式，绿色  
line_width = 2  
tick_length = 10  
font = cv2.FONT_HERSHEY_SIMPLEX  
font_scale = 0.5  
color = (0, 0, 255)  # BGR格式，红色

# 绘制X轴 
cv2.line(image, (0, 0), (width, 0), axis_color, line_width)   # 左上到右上
# 绘制Y轴  
cv2.line(image, (0, 0), (0, height), axis_color, line_width)  # 左上到右下

# 在坐标轴交点处绘制一个小圆点，作为原点标记（可选）  
cv2.circle(image, (0, 0), 5, axis_color, -1)    

# 绘制X轴刻度
x_ticks_interval = 80  # X轴刻度的间隔
for x in range(0, width, x_ticks_interval):
    # 绘制刻度线
    cv2.line(image, (x, 0), (x, tick_length), tick_color, line_width)
    # 绘制刻度标签
    cv2.putText(image, str(x), (x , 30), font, font_scale, color, line_width)
y_ticks_interval = 70
# 绘制Y轴刻度线和标签（已经是正确的从上往下递增）  
for y in range(height, 0, -y_ticks_interval):  
    # 绘制刻度线  
    cv2.line(image, (0, y), (tick_length, y), tick_color, line_width)     
    # 绘制刻度标签，直接显示y的值（从上往下递增）  
    cv2.putText(image, str(y), (15, y - 5), font, font_scale, color, line_width)

# 绘制实心圆所需的参数：圆心和半径  
circle_radius = 5  # 您可以根据需要调整这个值  
circle_color = (0, 255, 0)  # 这里使用绿色，但您可以自定义颜色  
circle_thickness = -1  # -1 表示实心圆

# 设置字体和颜色  
font = cv2.FONT_HERSHEY_SIMPLEX   
font_color = (255, 0, 0)  # 设置为蓝色，BGR格式  
line_type = 2  
  
# 在每个角点附近显示坐标  
for i, rectangle_corners in enumerate(rectangles_corners):
    for i, corner in enumerate(corners):   # enumerate函数可用来获取索引以及对应的内容
        # 将坐标转换为整数，因为putText期望整数坐标  
        x, y = map(int, corner)            
        # 格式化坐标字符串  
        text = f"{i+1}: ({x}, {y})"     # 格式化字符串坐标         
        # 计算文本大小  
        text_size, _ = cv2.getTextSize(text, font, font_scale, line_type)     
        # 在角 点旁边放置文本  
        text_x = x - text_size[0] // 2  
        text_y = y + text_size[1] // 2          
        # 在图像上放置文本  
        cv2.putText(image, text, (text_x, text_y), font, font_scale, font_color, line_type)   # （text_x,text_y为文本坐标）
        # 在角点上绘制实心圆  
        cv2.circle(image, (x, y), circle_radius, circle_color, circle_thickness)
# 显示结果  
cv2.imshow('Image', image)
cv2.imshow('edges',edges)  
cv2.waitKey(0)  
cv2.destroyAllWindows()