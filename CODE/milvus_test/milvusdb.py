from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
    AnnSearchRequest, RRFRanker, WeightedRanker,
    db
)

# Milvus向量数据库配置
class VectorDB:
    def __init__(self, collection_name="hybrid_search_collection", dim=1024, index_params={"index_type": "FLAT", "metric_type": "IP"}, sparse_index_params={"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "IP"}):
        self.collection_name = collection_name
        self.embedding_dim = dim  # 根据模型输出维度调整
        self.index_params = index_params
        self.sparse_index_params = sparse_index_params
        
        if not self._check_collection():
            self._create_collection()
            
        self.collection = Collection(self.collection_name)
    
    def _check_collection(self):
        return utility.has_collection(self.collection_name)
    
    def _create_collection(self):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="sparse_vectors", dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(name="dense_vectors", dtype=DataType.FLOAT_VECTOR, dim=self.embedding_dim),
        ]
        
        schema = CollectionSchema(fields, description="Document chunks with embeddings")
        self.collection = Collection(self.collection_name, schema, consistency_level="Strong")
        
        self.collection.create_index("sparse_vectors", self.sparse_index_params)
        self.collection.create_index("dense_vectors", self.index_params)
    
    def insert(self, text, sparse_vectors, dense_vectors):
        """存储文本块和嵌入向量"""
        entities = [
            text,  # text字段
            sparse_vectors,  # sparse_vectors字段
            dense_vectors,  # dense_vectors字段
        ]
        self.collection.insert(entities)
        self.collection.flush()
    
    def search(self, query_embedding, top_k=10, search_params={"metric_type": "IP"}, sparse_search_params={"metric_type": "IP"}):
        self.collection.load()
        """相似性搜索"""
        self.search_params = search_params
        self.sparse_search_params = sparse_search_params
        
        sparse_req = AnnSearchRequest(query_embedding["sparse"],
                              "sparse_vectors", self.sparse_search_params, limit=top_k)
        dense_req = AnnSearchRequest(query_embedding["dense"],
                             "dense_vectors", self.search_params, limit=top_k)
        
        results = self.collection.hybrid_search(
            [sparse_req, dense_req],
            rerank=RRFRanker(),
            limit=top_k,
            output_fields=["text"]
        )

        return [
                    {
                        "text": hit.entity.get('text'),
                        "distance": hit.distance
                    }
                    for hit in results[0]
                ] # [hit.entity.get('text') for hit in results[0]]