from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
    AnnSearchRequest, RRFRanker, WeightedRanker,
    db
)
import numpy as np
from FlagEmbedding import BGEM3FlagModel
from transformers import pipeline
import os
from datetime import datetime
import torch
from tqdm import tqdm

from milvusdb import VectorDB

devices = ["cuda:1"]
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
TARGET_DB = "test_db"  # 自定义数据库名称
COLLECTION_NAME="hybrid_search_collection"
EMBEDDING_MODEL_PATH = "/disk3/lsp/models/BAAI/bge-m3"

# 连接 Milvus
connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)

# 创建数据库（如果不存在）
if TARGET_DB not in db.list_database():
    print(f"数据库 {TARGET_DB} 不存在，创建数据库")
    db.create_database(TARGET_DB)
# 删除数据库
# db.drop_database(TARGET_DB)

# 切换当前数据库
db.using_database(TARGET_DB)
print("当前数据库：", TARGET_DB)
# 列出当前所有collection
print("当前数据库集合：", utility.list_collections())

def drop_collection(collection_name):
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)
        print(f"集合 {collection_name} 已删除")
    # for collection_name in utility.list_collections():
    #     utility.drop_collection(collection_name)
    #     print(f"Collection {collection_name} dropped.")

# 1. PDF文本解析与处理
def extract_text_from_pdf(pdf_dir):
    # 获取目录下所有pdf文件
    pdf_paths = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    data = []
    print("=====================================")
    print("PDF 文件数：", len(pdf_paths))
    # 逐个解析pdf文件
    for pdf_file in pdf_paths:
        print(f"解析 PDF ：{pdf_file}")
        loader = PyMuPDFLoader(pdf_file)
        data += loader.load()
    print('数据总数: ', len(data))
    return data

# 2. 文本分割
def split_documents(docs, chunk_size=1024, chunk_overlap=20):
    """使用LangChain的递归字符分割器"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", "；"]
    )
    
    return text_splitter.split_documents(docs)

# 3. 向量嵌入模型初始化
def init_embedding_model(model_dir="/disk3/lsp/models/BAAI/bge-m3", devices=["cuda:1"]):
    model = BGEM3FlagModel(model_dir, use_fp16=False, devices=devices)
    return model

# 4. 读取 PDF 文档并分割
def ingest_document(pdf_dir, batch_size=32):
    # 从 PDF 中提取文本
    docs = extract_text_from_pdf(pdf_dir)
    
    print('batch_size: ', batch_size)
    chunks = []
    for i in tqdm(range(0, len(docs), batch_size), desc="Splitting PDF into chunks"):
        batch_docs = docs[i:i+batch_size]
        chunks.extend(split_documents(batch_docs))
    print('chunks: ',len(chunks))
        
    
    # chunks = split_documents(docs)
    # print('chunks: ',len(chunks))

    texts = [doc.page_content for doc in chunks]
    return texts

# 5. 编码 文档，生成稠密和稀疏向量
def embed_documents(texts, embedder):
    embeddings = embedder.encode(
        texts,
        return_dense=True,
        return_sparse=True,
        return_colbert_vecs=False
    )
    dense_vecs = embeddings["dense_vecs"]
    sparse_vecs = embeddings["lexical_weights"]
    
    print('Embeddings length: ', len(dense_vecs))
    dim = len(dense_vecs[0])
    print('dim: ',dim)
    
    return dense_vecs, sparse_vecs, dim

# 6. 检索上下文
def search_context(question, embedder, vector_db, top_k=10, search_params={"metric_type": "IP"}, sparse_search_params={"metric_type": "IP"}):
    """检索上下文"""
    # 生成问题嵌入
    query_embedding_raw = embedder.encode(
        [question], 
        return_dense=True, 
        return_sparse=True, 
        return_colbert_vecs=False)
    
    query_embedding = {}
    query_embedding["dense"] = query_embedding_raw["dense_vecs"]
    query_embedding["sparse"] = [dict(query_embedding_raw["lexical_weights"][0])]
    
    # 向量数据库检索
    results = vector_db.search(query_embedding, top_k=top_k, search_params=search_params, sparse_search_params=sparse_search_params)
    return results


if __name__ == '__main__':
    # 清空集合
    drop_collection(COLLECTION_NAME)
    
    pdf_dir = './pdf'
    # 编码器初始化
    embedder = init_embedding_model(model_dir=EMBEDDING_MODEL_PATH, devices=devices)
    texts = ingest_document(pdf_dir, batch_size=32)
    dence_vecs, sparse_vecs, dim = embed_documents(texts, embedder)

    # Milvus向量数据库配置
    # 构建索引参数
    index_params = {
        "index_type": "FLAT",  # 无需参数配置
        "metric_type": "IP"    # 根据需求选 L2/IP/COSINE
        }
    sparse_index_params = {
        "index_type": "SPARSE_INVERTED_INDEX", 
        "metric_type": "IP"
        }
    # 搜索参数
    search_params = {"metric_type": "IP"}
    sparse_search_params = {"metric_type": "IP"}

    vector_db = VectorDB(collection_name=COLLECTION_NAME,dim=dim, index_params=index_params, sparse_index_params=sparse_index_params)
    vector_db.insert(texts, sparse_vecs, dence_vecs)
    
    question = "导演专业的主要工作内容是？"
    results = search_context(question, embedder, vector_db, top_k=10, search_params=search_params, sparse_search_params=sparse_search_params)
    context_chunks = [result['text'] for result in results]
    context = "\n".join(context_chunks)
    print("=====================================")
    print("问题：", question)
    # print("上下文：", context)
    print("文本块数：", len(context_chunks))