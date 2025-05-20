1. 修改数据外键：

```python
# 假设 parent_label 是外键
Label.objects.filter().update(parent_label=Label.objects.filter().first())
```

