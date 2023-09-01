1. 导入 `numpy`：

```python
import numpy as np
```

2. 创建 `array`：

```python
array = np.array([[1,2,3],
                  [1,2,3]])
print(array)
print(array.ndim) # 维度
print(array.shape) # (...,行,列,) 每一维的行数/列数
print(array.size) # 大小
# 指定类型
a = np.array([1,3,45],dtype=np.float64)
print(a.dtype)
# 创建全为 0
b = np.zeros((3,5),dtype=int)
# 创建全为 1
c = np.ones((3,5),dtype=np.int64)
# 创建对角全为 1 的对角阵
np.eye(3) # 方针
np.eye(3,4) # 3 行 4 列
np.eye(5,k=2) # k 指定对角偏移，可正可负
# 生成指定范围的整数数组，可通过 reshape 变成矩阵
d = np.arange(1,13).reshape(3,4)
# 生成指定范围、指定分段段数的数组，可通过 reshape 变成矩阵
e = np.linspace(1,10,6).reshape(2,3)
# 生成随机值组成的矩阵
a = np.random.random((3,4))
a = np.random.randn(3,4)
# 生成正态分布，loc 表示正态分布的均值，scale 表示正态分布的标准差，size 表示输出的值数量
numpy.random.normal(loc=0,scale=1e-2,size=shape)
```

3. `array` 基础运算：

```python
a + b # 逐位运算，范围运算结果的 array
b**2 # 幂
np.sin(a) # 三角运算
(b < 3) # 逐位比较，返回一个 boolean 值组成的 array
(a == b) # 逐位比较，返回一个 boolean 值组成的 array
a * b # 同位相乘
np.dot(a,b) # 矩阵乘法，也可用 a.dot(b)

np.all(a) / np.any(a) # 值是否全为 True / 存在 True，返回 boolean 值
np.any(a,axis-0) # axis 指定对 (...,列,行) 中哪一维进行操作，返回 boolean 值组成的 array

np.sum(a, axis=0) # axis 指定对 (...,列,行) 中哪一维进行操作
np.min(a, axis=1)
np.max(a)
np.argmin(a) # 返回最小值索引
np.argmax(a)
np.mean(a) # 求平均值，也可用 a.mean()
np.median(a) # 中位数
np.percentile(a, 25) # 下 4 分位数，可用第二位改变百分比
np.cumsum(a) # 累加，返回一维 array ，其中第 i 位为前 i 个数累加
np.diff(a) # 邻位相减，返回矩阵，每一行的第 i 个数为第 i+1 个数减去第 i 个数，估每行长度减 1

np.nonzero(a) # 返回 a 中非零元素索引值，每一维的索引值对应一个 array ，是一个多 array 的 tuple
np.transpose(np.nonzero(a)) # 将上述多 array 组合成矩阵，实际上是转置
a[np.nonzero(a)] # 返回 a 中所有非零元素构成的 array，实际上是索引

np.sort(a) # 排序，对每一行进行排序
np.transpose(a) # 转置，可简写为 a.T
a.transpose((2,1,0)) # 高维转置，本质为置换坐标轴，这里 (...,n-1,n) 对应 (...,列,行)

np.clip(a,5,9) # 对 a 中 ≤ 5 的数都置为 5，≥ 9 的数都置为 9，5 与 9 之间的数不变

b = np.array([1,1,1])
b.T # 一维无法转置，即仍返回 [1 1 1]
b[np.newaxis,:] # 按行升维，相当于变为 [[1 1 1]]
b[:,np.newaxis] # 按列升维，相当于变为 [[1]
				#                    [1]
				#                    [1]]
```

4. 索引：

```python
a[2,1] # 等同于 a[2][1]
a[[2],[1]] # 返回的是一个 array ，等同于 np.array([a[2][1]])
a[2,:]
for row in a: # 迭代每一行
for item in a.flat: # 迭代每个元素，a.flat 将 a 转化为一个迭代器
a.flatten() # 将 a 转为一个一维 array
```

5. 合并 `array`：

```python
np.vstack((a,b)) # 垂直合并，相当于直接合并
np.hstack((a,b)) # 水平合并，相当于对应元素合并，如：
                 # a = [[1 1 1]
                 #      [2 2 2]]
                 # b = [[2 2 2]
                 #      [3 3 3]]
                 # vstack 拼接后：
                 # [[1 1 1]
				 #  [2 2 2]
				 #  [2 2 2]
				 #  [3 3 3]]
                 # hstack 拼接后：
                 # [[1 1 1 2 2 2]
                 #  [2 2 2 3 3 3]]
        
np.concatenate((a,b,c,...),axis=0) # 用 axis 指定对 (...,列,行) 中哪一维进行操作
# 注意：对于一维 array，np.vstack() 进行垂直合并时可以直接将其变为二维，
# 	   而 np.concatenate() 只能指定 axis = 0 进行水平合并
```

6. 分割`array`：

```python
np.split(a, n, axis=0) # 分割成相等大小的 n 块 array，只能整分
np.array_split(a, n, axis=0) # 对于无法整分的，向上取整，故最后几块会小一点
np.vsplit(a,3) # 垂直分割，只能整分
np.hsplit(a,3) # 水平分割，只能整分	
```

7. `copy`和`deepcopy`：

```python
b = a # 浅拷贝，a、b 指向同一块地址
b = a.copy() # 深拷贝
```

