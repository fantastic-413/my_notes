##### 1、`pickle` 存放数据：

```python
with open('pickle_test.pickle','wb') as file:
	pickle.dump(data,file)
with open('pickle_test.pickle','rb') as file:
    data = pickle.load(file)
```

##### 2、两大法宝函数：

```python
dir() # 列出某个类或者某个模块中的全部内容，包括变量、方法、函数和类等
help() # 查看某个函数或者模块的帮助文档
```

##### 3、图片格式：

```python
# CHW：C 为通道(channel)，H 为高度，W 为宽度。
# RGB：B(蓝)，G(绿)，R(红) 分别为 3 通道时的 0，1，2 位置。
# numpy 包的图片是: H*W*C，而 torch 包的图片是: C*H*W

# cv2读取图片, 返回 numpy.ndarray 格式，维度为 HWC，颜色通道为 BGR
# cv2读取图片后转 CHW 和 RGB：img[:,:,::-1].transpose((2,0,1))
# img[:,:,::-1] 表示把 BGR 转为 RGB
# transpose((2,0,1)) 表示把 HWC 转为 CHW
```

##### 4、`class` 内置函数：

```python
def __init__(self[, name,...]) # 初始化类时使用，如 person = Person("lishipeng1")
def __getitem__(self, index) # 通过索引如 person[idx] 时调用该函数获取返回值
def __len__(self) # 通过全局函数 len(person) 时调用获取返回值
def __call__(self[, age,...]) # 通过实例直接传参如 person(27) 时调用该函数
```

##### 5、python yield用法

[python中yield的用法详解](https://blog.csdn.net/mieleizhi0522/article/details/82142856/)

##### 6、python @staticmethod和@classmethod的用法

[@staticmethod和@classmethod的用法](https://blog.csdn.net/polyhedronx/article/details/81911548)

##### 7、`filter`()函数用法

`filter(函数,序列)`函数：

- 该函数接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判断，然后返回 True 或 False，最后将返回 True 的元素放到新列表中。

##### 8、	
