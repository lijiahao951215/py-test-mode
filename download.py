from sentence_transformers import SentenceTransformer

# 下载模型（会自动从 HuggingFace 下载）
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# 保存模型到本地目录，例如：./all-MiniLM-L6-v2
model.save('./models/all-MiniLM-L6-v2')