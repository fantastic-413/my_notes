from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
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
import argparse
import pandas as pd

from milvusdb import VectorDB

devices = ["cuda:1"]
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
TARGET_DB = "test_db"  # 自定义数据库名称
COLLECTION_NAME="hybrid_search_collection"
EMBEDDING_MODEL_PATH = "/disk3/lsp/models/BAAI/bge-m3"
DIM = 1024

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

# PDF文本解析与处理
def extract_text_from_pdf(pdf_path):
    print(f"解析 PDF ：{pdf_path}")
    loader = PyMuPDFLoader(pdf_path)
    data = loader.load()
    return data

# EXCEL文本解析与处理
def extract_text_from_excel(excel_path):
    # print(f"解析 Excel ：{excel_path}")
    # loader = UnstructuredExcelLoader(excel_path, mode="elements")
    # data = loader.load()
    # return data
    
    # # 读取excel文件
    df = pd.read_excel(excel_path)
    # data = df.to_string(index=False)
    # # 提取纯列名行（第一行）
    # header_line = data.split('\n')[0] + '\n'  # 带换行符
    # docs = [Document(page_content=data, metadata={"file_path": excel_path})]
    # return docs, header_line
    
    # 方法2：逐行生成多个Document（推荐用于检索场景）
    docs_multiple = []
    for _, row in df.iterrows():
        content = "\n".join([f"{col}: {row[col]}" for col in df.columns])
        docs_multiple.append(Document(
            page_content=content,
            metadata={"file_path": file_path, "columns": list(df.columns)}
        ))
    return docs_multiple

# 文件处理器映射表
FILE_PROCESSORS = {
    '.pdf': extract_text_from_pdf,
    '.xlsx': extract_text_from_excel,
}

# 文本分割
def split_documents(docs, chunk_size=1024, chunk_overlap=20):
    """使用LangChain的递归字符分割器"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", "；"]
    )
    
    return text_splitter.split_documents(docs)

# 向量嵌入模型初始化
def init_embedding_model(model_dir="/disk3/lsp/models/BAAI/bge-m3", devices=["cuda:1"]):
    model = BGEM3FlagModel(model_dir, use_fp16=False, devices=devices)
    return model

# 读取 PDF 文档并分割
def ingest_document(docs, batch_size=256):
    print('Split chunks\' batch_size: ', batch_size)
    chunks = []
    for i in tqdm(range(0, len(docs), batch_size), desc="Splitting PDF/EXCEL into chunks"):
        batch_docs = docs[i:i+batch_size]
        chunks.extend(split_documents(batch_docs))
    print('chunks: ',len(chunks))
        
    
    # chunks = split_documents(docs)
    # print('chunks: ',len(chunks))

    texts = [doc.page_content for doc in chunks]
    return texts

# 编码文档，生成稠密和稀疏向量
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

# 检索上下文
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
    
    file_dir = './excel'
    # 编码器初始化
    embedder = init_embedding_model(model_dir=EMBEDDING_MODEL_PATH, devices=devices)
    
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

    vector_db = VectorDB(collection_name=COLLECTION_NAME,dim=DIM, index_params=index_params, sparse_index_params=sparse_index_params)
    
    # 获取目录下所有 pdf/excel 文件
    file_paths = [os.path.join(file_dir, f) for f in os.listdir(file_dir)]
    print("=====================================")
    print(f"待解析文件数：", len(file_paths))
    # 逐个解析pdf文件
    for file_path in file_paths:
        print("-"*20)
        print(f"解析文件：{file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        processor = FILE_PROCESSORS.get(ext)
        if not processor:
            print(f"文件 {file_path} 无法解析")
            continue
        
        data = processor(file_path)
        # 逐个插入文档
        texts = ingest_document(data, batch_size=32)
        dence_vecs, sparse_vecs, _ = embed_documents(texts, embedder)

        for i in tqdm(range(0, len(texts), 1024), desc="Inserting batches into VectorDB"):
            batch_texts = texts[i:i+1024]
            batch_dense_vecs = dence_vecs[i:i+1024]
            batch_sparse_vecs = sparse_vecs[i:i+1024]
            vector_db.insert(batch_texts, batch_sparse_vecs, batch_dense_vecs)
        # vector_db.insert(texts, sparse_vecs, dence_vecs)
        
        print(f"文件 {file_path} 已插入")
        print("-"*20)
    
    question = "导演专业的主要工作内容是？"
    results = search_context(question, embedder, vector_db, top_k=10, search_params=search_params, sparse_search_params=sparse_search_params)
    context_chunks = [result['text'] for result in results]
    context = "\n".join(context_chunks)
    print("=====================================")
    print("问题：", question)
    # print("上下文：", context)
    print("文本块数：", len(context_chunks))