import os

import cv2
import numpy as np


def convert_npy_to_png(root_path, out_path):
    # 检查输出路径是否存在，如果不存在，则创建
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    # 遍历root_path下的所有.npy文件
    for file_name in os.listdir(root_path):
        if file_name.endswith('.npy'):
            # 构建完整的文件路径
            full_path = os.path.join(root_path, file_name)
            # 加载.npy文件
            data = np.load(full_path)
            # 确保数据是在合适的范围内
            if data.max() > 1:
                data = data.astype(float) / 255.0  # 转换为浮点数并归一化
            # 初始化累加数组
            accumulated_image = np.zeros_like(data[0])
            # 叠加所有图像
            for img in data:
                accumulated_image += img
            # 将累加值平均化
            accumulated_image = accumulated_image/len(data)
            # 检查最大值，如果小于等于1，则将其转换为0-255范围内的uint8
            if accumulated_image.max() <= 1:
                accumulated_image = (accumulated_image * 255).astype(np.uint8)
            # 使用OpenCV调整图像大小到512x512
            resized_image = cv2.resize(accumulated_image, (32,32), interpolation=cv2.INTER_CUBIC)
            # 构建输出文件名和路径
            output_file_path = os.path.join(out_path, f"{os.path.splitext(file_name)[0]}.png")
            # 保存调整大小后的图像
            cv2.imwrite(output_file_path, resized_image)
            print(f"Image saved: {output_file_path}")

#读入，输出
convert_npy_to_png('E://pos/Spect_heart', 'E://pos/testpic')
