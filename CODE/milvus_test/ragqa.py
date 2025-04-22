from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
    AnnSearchRequest, RRFRanker, WeightedRanker,
    db
)
from milvusdb import VectorDB
from openai import OpenAI
from createdb import search_context, init_embedding_model, devices, COLLECTION_NAME

embedder = init_embedding_model(devices=devices)
search_params = {"metric_type": "IP"}
sparse_search_params = {"metric_type": "IP"}

vector_db = VectorDB(collection_name=COLLECTION_NAME)

openai_api_key = "token-abc123"
openai_api_base = "http://10.249.42.98:8000/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
    
)

# 进行问答
while True:
    query = input("\n请输入问题（输入q退出）: ")
    if query.lower() == 'q':
        break
    
    results = search_context(query, embedder, vector_db,  top_k=2, search_params=search_params, sparse_search_params=sparse_search_params)
    context_chunks = [result['text'] for result in results]
    context = "\n".join(context_chunks)
    # 生成答案
    prompt = f"""请仅根据给定上下文回答问题。\n上下文：\n{context}\n问题：{query}\n答案："""
    completion = client.chat.completions.create(model="/llm/Qwen2.5-32B-Instruct", messages=[
            {"role": "system", "content": "请仅根据给定上下文回答问题。"},
            {"role": "user", "content": f"上下文：\n{context}\n问题：{query}\n答案："},
        ]
    )
    anwser = completion.choices[0].message.content
    print("=====================================")
    print("问题：", query)
    print("上下文：", context)
    print("答案：", anwser)