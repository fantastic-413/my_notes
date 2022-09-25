1. `pickle` 存放数据：

```python
with open('pickle_test.pickle','wb') as file:
	pickle.dump(data,file)
with open('pickle_test.pickle','rb') as file:
    data = pickle.load(file)
```

