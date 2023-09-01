# 基础操作：

```python
# 获取路径
os.path.abspath(path) # 返回 path 的绝对路径
os.getcwd() # 获取当前文件所在的绝对路径
os.path.commonprefix(path_list) # 返回 path_list 中所有路径的公共路径
os.path.relpath(path) # 返回 path 相对于当前程序的相对路径
os.chdir(path) # 跳转当前文件路径，path 需要是已经存在的路径

# 新建/删除/修改
os.rename(src,dst) # 修改文件/目录名
os.mkdir(path) # 新建目录，只能一级一级新建
os.makedirs(path) # 可新建多级目录
os.remove(path) # 删除文件
os.rmdir(path) # 删除目录，只能一级一级删除，目录必须为空
os.removedirs(path) # 可删除多级目录，目录必须为空
import shutil
shutil.rmtree(path) # 可删除非空目录，递归删除目录

# 获取文件/目录
os.path.getsize(path) # 返回 path 文件的字节大小
os.listdir(path) # 返回指定目录下所有文件名称的 list
next(os.walk(path)) # 返回 (path，文件夹名称 list，文件名称 list) 

# 判断
os.path.exists(path) # 返回路径是否存在
os.path.isdir(path) # 返回是否是文件夹
os.path.isfile(path) # 返回是否是文件
os.path.isabs(path) # 返回是否是绝对路径

#合并
os.path.join(root_path, label_path) # 将路径合并起来

# 拆分
os.path.splitdrive(path) # 将 path 中的磁盘和路径拆分出来，以 ('E:', '\\test.py') 返回
os.path.splitext(path) # 将 path 中最后一个文件的扩展名拆分出来，以 ('E:\\test', '.py') 返回
os.path.split(path) # 将 path 中最后一个文件/目录名称拆分出来，以 ('E:\\', 'test.py') 返回
os.path.dirname(path) # 返回 path 的路径，即 os.path.split(path) 返回值的第一个元素
os.path.basename(path) # 返回 path 的文件名，即 os.path.split(path) 返回值的第二个元素
```

