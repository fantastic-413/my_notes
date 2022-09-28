1. 安装地址：[Pytorch官网](https://pytorch.org/get-started/locally/)

2. 测试是否安装成功（GPU）：

```python
import torch
torch.cuda.is_available() # cuda 是否可用
torch.cuda.device_count() # 返回 gpu 数量
torch.cuda.get_device_name(0) # 返回 gpu 名字，设备索引默认从 0 开始
torch.cuda.current_device() # 返回当前设备索引
```

