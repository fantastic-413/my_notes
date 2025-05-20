1. 导入 `pandas`：

```python
import pandas as pd
```

2. 创建 `DateFrame`：

```python
# Series 一维数组
s = pd.Series([1,3,6,np.nan,44,1])
s = pd.Series({'a':10,'b':20,'c':30,'d':40,'e':50}) # 通过字典，key 为行名
index = ['Bob', 'Steve', 'Jeff', 'Ryan', 'Jeff', 'Ryan']
s = pd.Series([4, 7, -5, 3, 7, np.nan],index = index) # 通过 index 指定行名

# DataFrame(数据[,index=行名称,columns=列名称])
dates = pd.date_range('20220920',periods=6)
df = pd.DataFrame(np.random.randn(6,4),index=dates,columns=['A','B','C','D'])
# DataFrame(字典类型)，其中 key 为列名，value 会对齐最长行补全
df = pd.DataFrame({
    'A': 1,
    'B': np.array([3]*4,dtype=int),
    'C': pd.Timestamp('20220920'),
    'D': pd.Categorical(['test','train','hi','hello']),
    'F': 'hihihi'
})
```

3. 基础操作：

```python
df.dtypes
df.index # 行名称序列
df.columns # 列名称序列
df.values # 值 array

df.describe() # 返回数据中数值列的 count(个数), mean, std(标准差), min, 25%, 50%, 75%, max
df.T # 转置

# 对行列名称排序，axis 指定 (行名称,列名称)，ascending 指定升降序
df.sort_index(axis=1, ascending=false)
# 对值排序，by 指定行/列名称，axis指定 (列,行)，ascending 指定升降序
df.sort_index(by='D',axis=1, ascending=false)
```

4. 选择数据：

```python
df['A']
df[['A','B']]
df.A # 选择对应列，'df.列名' 对数值的列名无法使用

df[0:3]
df['20220920':'20220922'] # 选择对应行，只能通过切片形式 [:] ,而无法直接选取

df[0:3][0:3]
df[0:3][['A','B']] # 选择对应行列

# select by label，即无法通过 position 数值来筛选
df.loc['20220923':'20220925','B':'D']
df.loc[['20220920','20220922'],['A','B']]

# select by position，即无法通过 label 名称来筛选
df.iloc[0:3,1:3]
df.iloc[[0,2],[1,3]]

df[df.A > 8] # 返回满足条件的元组
```

5. 设置值：

```python
df[df.A > 8] = 0 # 将满足条件的元组的所有值设置为 0
df.B[df.A > 4] = 0 # 将满足条件的元组的 'B' 列设置为 0 

df['F'] = np.nan # 新增一个 'F' 列，值全为 NaN
df['E'] = pd.Series([1,2,3,4,5,6],index=pd.date_range('20220920',periods=6))
# 使用 Series 一维数组赋值时，需要行名相同
```

6. 处理丢失数据：

>  `df.dropna()` 中的 `axis` 参数与其余的不同，==`axis=0/1` 表示的是**0行/1列**==

```python
# 以下都不会改变原 DataFrame
df.dropna(axis=1,how='any') # 返回值中去除 NaN 值所在的 axis 指定 (行,列)，
                            # how='any'(有 NaN 就去掉)/'all'(所有值都为 NaN 才去掉)
df.fillna(value=999) # 返回值中把 NaN 值换为 999
df.isna() / df.isnull() # 返回值中 NaN 值换为 True，其余为 False
# 判断部分缺失值/全部缺失
np.any(df.isna()) / np.all(df.isna())
```

7. 导入导出：

```python
data = pd.read_csv('2019fpx.csv') # 导入 csv 文件
data.to_pickle('2019fpx.pickle') # 导出为 pickle 文件
```

8. 合并 `DataFrame`：

```python
# 用 axis 指定对 (...,列,行) 中哪一维进行操作
# 用 ignore_index 忽略掉所有行名称 index，对合并的结果重新生成行名称 index
pd.concat([df1,df2,df3,...],axis=0,ignore_index=True)

# join 默认为 outer，若为 inner(内连接) 且 axis=0 则会选取列名称相同的数据进行合并
pd.concat([df1,df2,df3,...][,join='inner'])

# merge() 只能水平合并
# on 指定基于 key1 和 key2 列相同值进行合并，有列名相同的可以不指定 on
# how 默认 inner(内连接)，还可以取 outer(外) / left(左) / right(右)
# indicator 设置是否显示数据来源，可为 True 或 自定义名称
pd.merge(left,right,on=['key1','key2'],how='inner')

# 用 left_index/right_index 指定按照 index(行) 来合并，且会区分相同的列名
# 如 key_x、key_y 区分来自左、右数据的列
pd.merge(left,right,left_index=True,right_index=True,how='inner',indicator=True)

# 用 left_on/right_on 指定按照 列 来合并，且会区分相同的列名
# 如 key_x、key_y 区分来自左、右数据的列
pd.merge(left,right,left_on='X',right_on='Y',how='outer',indicator=True)

# 用 suffixes 指定相同列名的后缀取值
# 如 key2_left、key2_right 区分来自左、右数据的列
pd.merge(left,right,on=['key1'],suffixes=['_left','_right'])
```

9. `plot` 画图：

```python
import matplotlib.pyplot as plt
data.plot()
plt.show()
```

