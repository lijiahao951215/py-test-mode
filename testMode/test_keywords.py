from flask import Flask, request, jsonify
from keybert import KeyBERT

app = Flask(__name__)

# 初始化 KeyBERT 模型
kw_model = KeyBERT('all-MiniLM-L6-v2')

@app.route("/keywords", methods=["POST"])
def extract_keywords():
    try:
        data = request.get_json()
        product_name = data.get("product_name", "").strip()
        top_n = int(data.get("top_n", 5))

        if not product_name:
            return jsonify({"error": "Missing 'product_name'"}), 400

        # 提取关键词
        keywords = kw_model.extract_keywords(
            product_name,
            keyphrase_ngram_range=(1, 2),
            stop_words='english',
            top_n=top_n
        )

        return jsonify({
            "product_name": product_name,
            "keywords": [kw[0] for kw in keywords]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
