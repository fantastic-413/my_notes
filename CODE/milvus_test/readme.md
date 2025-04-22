## 安装milvus
```python
# Download the installation script
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh

# Start the Docker container
bash standalone_embed.sh start
```

## 停止、删除与更新
```python
# Stop Milvus
bash standalone_embed.sh stop
# Delete Milvus data
bash standalone_embed.sh delete
# upgrade Milvus
bash standalone_embed.sh upgrade
```