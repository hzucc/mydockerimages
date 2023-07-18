import cv2
import numpy as np


print(cv2.cuda.getCudaEnabledDeviceCount())

# 生成模板和图像
template = np.zeros((100, 100), dtype=np.uint8)
template[25:75, 25:75] = 255
image = np.zeros((480, 640), dtype=np.uint8)
image[200:300, 200:300] = 255

# 创建 GPU 上的图像和模板
gpu_image = cv2.cuda_GpuMat()
gpu_template = cv2.cuda_GpuMat()
gpu_image.upload(image)
gpu_template.upload(template)

# 创建结果图像和 GPU 上的结果图像
# 创建模板匹配器
matcher = cv2.cuda.createTemplateMatching(gpu_image.type(), cv2.TM_SQDIFF_NORMED)

# 在GPU上进行模板匹配
result_gpu = matcher.match(gpu_image, gpu_template)

result = result_gpu.download()

res = cv2.minMaxLoc(result)
print(res)

