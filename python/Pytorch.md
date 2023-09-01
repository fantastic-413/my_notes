1. 安装地址：[Pytorch官网](https://pytorch.org/get-started/locally/)

2. 测试是否安装成功（GPU）：

```python
import torch
torch.cuda.is_available() # cuda 是否可用
torch.cuda.device_count() # 返回 gpu 数量
torch.cuda.get_device_name(0) # 返回 gpu 名字，设备索引默认从 0 开始
torch.cuda.current_device() # 返回当前设备索引
```

3. `Dataset`：

```python
# 导入
from torch.utils.data import Dataset
from PIL import Image # 图片处理	
import os # 处理文件和目录


# Dataset是一个抽象类，实际使用中需要继承Dataset，
# 重写 __len__() 方法，实现通过全局的 len() 方法获取其中的元素个数
# 重写 __getitem__(idx) 方法，实现通过索引获取数据。
	# 如 dataset[idx] 获取其中的第 idx 条数据的内容及 label
class MyData(Dataset):
    
    def __init__(self, root_dir, label_dir):
        self.root_dir = root_dir
        self.label_dir = label_dir
        self.path = os.path.join(self.root_dir, self.label_dir)
        self.img_path = os.listdir(self.path)
        
    def __getitem__(self,idx):
        img_name = self.img_path[idx]
        img_item_path = os.path.join(self.path, img_name)
        img = Image.open(img_item_path)
        label = self.label_dir
        return img,label
    
    def __len__(self):
        return len(self.img_path)
    
dataset = MyData("root", "label")
img, label = dataset[0]
```

4. `Dataloader`:

> - Epoch： **所有**训练样本都已输入到模型中，称为一个 Epoch
> - Iteration：**一批**样本输入到模型中，称为一个 Iteration
> - Batchsize： **批大小**

```python
# 导入
from torch.utils.data import DataLoader

# dataset: Dataset 类，决定数据从哪读取以及如何读取
# batch_size: 传入数据的 batch 大小，常常是 32、64、128、256
# shuffle: 每个 epoch 是否乱序
# num_workers: 加载数据的线程数
# drop_last: 当样本数不能被batchsize整除时，是否舍弃最后一批数据
	# 如样本总数是 87， batch_size==8：
	# drop_last = False，则 1 Epoch = 11 Iteration，最后一个 Iteration 为 7 个样本
	# drop_last = True，则 1 Epoch = 10 Iteration，舍弃最后 7 个样本
dataloder = DataLoader(dataset, batch_size=2, shuffle=False, num_workers=0，
                       drop_last=False)
```

5. `tensorboard`：

```python
# 导入
from torch.utils.tensorboard import SummaryWriter

# 创建对象
writer = SummaryWriter("logs") # 定义 logs 文件所在文件夹位置
writer = SummaryWriter() # 在当前目录自动生成文件夹名
writer = SummaryWriter(comment='test') # 在当前目录自动生成的文件夹名，附带 comment 作为后缀

# tag (string): 数据标题/标签
# scalar_value (float or string/blobname): 数据值 (y 轴)
# global_step (int): 全局步长值 (x 轴)
writer.add_scalar(tag,scalar_value,global_step)

# tag (string): 数据标题/标签
# img_tensor (torch.Tensor, numpy.array, or string/blobname): 图像数据
# global_step (int): 全局步长值 step，可用不同的 step 使图片组合在一个框里，滑动选择
# dataformats：如 CHW , HWC , HW。
# img_tensor：默认为 (3,H,W) 。您可以使用 torchvision.utils.make_grid() 将一批张量转换为 		 3*H*W 格式。非 (3,H,W) 格式需要使用 dataformats=''
writer.add_image(tag, img_tensor, global_step, dataformats)

# 关闭
writer.close()

# 打开命令行输入以下命令，并点击网址即可
# logdir=相对路径/绝对路径
tensorboard --logdir=logs [--port=xxxx]
```

6. `transform`：

```python
# 导入
from torchvision import transforms

# 单个使用
# ToTensor()：转为 torch.tensor 类型
	# 首先从 transforms 中选择一个 class 进行实例化创建
	# 再传入相应参数 img 使用
trans_totensor = transforms.ToTensor()
img_tensor = trans_totensor(img)

# Normalize()：归一化
	# mean：(mean[1],...,mean[n])，均值，n 为通道(channel)数
    # std：(std[1],..,std[n])，标准差，n 为通道(channel)数
    # 归一化：output[channel] = (input[channel] - mean[channel]) / std[channel]
    # 传入参数 img_tensor 应为 tentor 类型
trans_norm = transforms.Normalize(mean, std)
img_norm = trans_norm(img_tensor)

# Resize()：调整大小
	# size：可以是序列如 (h,w)，也可以是单个 int 数字，按 (h,w) 较小的一个变成 size 进行放缩
    # 再传入相应参数 img 使用，img 可为 PILImage(再使用 ToTensor 转为tensor) 或 tensor
trans_resize = transforms.Resize(size)
img_resize = trans_resize(img)

# RandomCrop()：随机位置裁剪
	# size：可以是序列如 (h,w)，也可以是单个 int 数字，按 (size,size) 进行裁剪
# CenterCrop()：中心位置裁剪
	# size：可以是序列如 (h,w)，也可以是单个 int 数字，按 (size,size) 进行裁剪

# 组合使用
# Compose()，分别使用每个 class 对 img 进行操作
trans_compose = transforms.Compose([transforms.Resize(size), transforms.ToTensor()])
img = trans_compose(img)
```



`model.eval()`：[model.eval()用法详解](https://blog.csdn.net/sazass/article/details/116616664)

不启用 `BatchNormalization` 和 `Dropout`，保证 `BN` 和 `dropout` 不发生变化，`pytorch` 框架会自动把 `BN` 和 `Dropout` 固定住，不会取平均，而是用训练好的值，不然的话，一旦 `test` 的 `batch_size` 过小，很容易就会被 `BN` 层影响结果。
