1. 导入并连接：

```python
from py2neo import *
graph = Graph("http://127.0.0.1:7474",auth=("账号","密码"))
```

2. 新建节点与关系：

```python
# 头实体
head = Node("head_label", name='head_name')
# 尾实体
tail = Node("tail_label", name='tail_name')
# 关系
relation = Relationship(head, "relation_name", tail)
# 创建关系（连带创建节点）
graph.create(relation)
```

3. 创建时合并相同节点：

```python
node_list = list(matcher.match("node_label",name='node_name'))
if len(node_list) > 0:
    node = node_list[0]
else:
    node = Node("node_label",name='node_name')
graph.create(node)
```

4. 查询节点与关系：

```python
data_list = list(graph.match(r_type="relation_name") # 返回关系三元组

matcher = NodeMatcher(graph) # 用于查询节点
node_list = list(matcher.match("node_label",name='node_name')) # 返回节点
r_matcher = RelationshipMatcher(g) # 用于查询关系
relation_list = list(r_matcher.match(nodes=[fugui, youqian])) # 返回关系三元组
                  					# 这里的 node 参数也可以是none,表示任意节点。注意前后顺序
                					# 也可用 rtype
node = matcher[node_id] # 根据 id 查询节点
node = graph.nodes[node_id]
                
graph.nodes # 所有节点
graph.relationships # 所有关系
graph.nodes.match("node_label",name='node_name') # 查询指定节点
```

5. 追加属性与删除属性：

```python
# 以下同样适用于 relation
node_list = list(matcher.match("node_label",name='node_name'))
# setdefault() 如果此节点具有属性 'age'，则返回其值。如果没有，添加 'age' 属性和对应的属性值 '30'
node.setdefault('age',default='30')
node_list[0]['home'] = 'jiangxi' # 新增属性 'home' 和对应的属性值 'jiangxi'
node_list[0].remove_label('age') # 删除属性
graph.push(node_list[0]) # 提交更改

# 属性批量更新
atrributes = { 'name': 'Amy', 'age': 23 } 
node.update(atrributes) 
```

6. 事务与批处理：

```python
tx = graph.begin() # 创建事务
tx_list = Subgraph(nodes=node_list, relationships=relation_list)
tx.create(tx_list)
graph.commit(tx) # 提交事务
```

7. 删除节点和关系：

```python
graph.delete_all() # 删除所有节点和关系
graph.delete(node) # 删除指定节点
graph.delete(relation) # 删除指定关系及节点
graph.separate(relation) # 仅删除关系
```

8. 其余操作：

```python
# 以下同样适用于 relation
node.idendity # 节点 id
node[key] # 获取 key 对应的属性值
node[key] = value # 设置 key 键对应的 value，如果 value 是 None 就移除这个属性
del node[key] # 删除某个属性
len(node) # 返回 node 里面属性的个数
labels = node.labels # 返回所以和这个节点有关的属性
node.labels.remove(labelname) # 删除某个属性
dict(node) # 将 node 的所有属性以 字典 的形式返回


graph.schema.node_labels # 查询所有节点标签，
						 # 返回值为 frozenset({'company', 'skill', 'item', 'employee'})
graph.schema.relationship_types # 查询所有关系名称，
						 # 返回值为 frozenset({'item_of', 'skill_of', 'work_in'})
    
node_list.to_data_frame() # 返回 dataframe 格式，也可直接 pd.dataframe(node_list)
node_list.data() # 返回字典格式
node_list.to_ndarray() # 返回 numpy 数据
```

9. 使用 `cyper(CQL)` 语句：

```python
graph.run('MATCH (p:Person) return p')
graph.run('MATCH (n) DETACH DELETE n')
```

