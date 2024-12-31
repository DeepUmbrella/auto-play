import cv2
import numpy as np

# 读取图片
b_image = cv2.imread('datasets/Screen.png')  # 主图片
a_image = cv2.imread('datasets/start_game.png')  # 模板图片
c_image = cv2.imread('datasets/gameover.png')  # 模板图片
d_image = cv2.imread('datasets/create_role.png')  # 模板图片

# 转为灰度图像（如果是彩色图像）
b_gray = cv2.cvtColor(b_image, cv2.COLOR_BGR2GRAY)
a_gray = cv2.cvtColor(a_image, cv2.COLOR_BGR2GRAY)
c_gray = cv2.cvtColor(c_image, cv2.COLOR_BGR2GRAY)
d_gray = cv2.cvtColor(d_image, cv2.COLOR_BGR2GRAY)

# 使用模板匹配


# 获取匹配结果的最大值和位置
def get_pos(main_gray, target_gray):
    result = cv2.matchTemplate(main_gray, target_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # max_loc 是匹配位置的左上角坐标
    top_left = max_loc

    # 计算右下角坐标
    height, width = target_gray.shape
    bottom_right = (top_left[0] + width, top_left[1] + height)

    return top_left, bottom_right


top_left, bottom_right = get_pos(b_gray, a_gray)
top_left1, bottom_right1 = get_pos(b_gray, c_gray)
top_left2, bottom_right2 = get_pos(b_gray, d_gray)

# 在 b 图片中绘制匹配区域
cv2.rectangle(b_image, top_left, bottom_right, (0, 255, 0), 2)
cv2.rectangle(b_image, top_left1, bottom_right1, (0, 255, 0), 2)
cv2.rectangle(b_image, top_left2, bottom_right2, (0, 255, 0), 2)

# 显示结果
cv2.imshow('Matched Result', b_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
