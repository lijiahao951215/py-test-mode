from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/user/<username>')
def show_user_profile(username):
    # 显示用户的个人资料
    return f'User {username}'

# ✅ 加入 SBERT 模型和产品数据
# model = SentenceTransformer('all-MiniLM-L6-v2')
model = SentenceTransformer('/www/wwwroot/py-test-mode/models/all-MiniLM-L6-v2')

# ✅ 新增的 /similarity 路由
@app.route("/similarity", methods=["POST"])
def similarity():
    try:
        data = request.get_json()
        query = data.get("product_name", "").strip()
        compare_products = data.get("products", [])
        top_k = int(data.get("top_k", 5))

        if not query:
            return jsonify({"error": "Missing 'product_name'"}), 400
        if not compare_products or not isinstance(compare_products, list):
            return jsonify({"error": "Missing or invalid 'products' list"}), 400

        # 编码
        product_embeddings = model.encode(compare_products, convert_to_tensor=True)
        query_embedding = model.encode(query, convert_to_tensor=True)

        # 相似度
        scores = util.cos_sim(query_embedding, product_embeddings)[0]
        top_results = scores.topk(min(top_k, len(compare_products)))

        results = []
        for score, idx in zip(top_results.values, top_results.indices):
            product_name = compare_products[idx]
            if product_name.lower() == query.lower():
                continue
            results.append({
                "product": product_name,
                "score": round(score.item(), 4)
            })

        return jsonify({
            "query": query,
            "results": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


complement_map = {
    "Laptop": ["Mouse", "Keyboard", "Monitor", "USB Hub"],
    "Shoe": ["Socks", "Shoe Polish", "Insole"],
    "Short sleeve": ["Shorts", "Cap", "Sunglasses"]
}

# ✅ 新增的 /complementary 路由 互补产品 需要自己加映射
@app.route("/complementary", methods=["POST"])
def complementary():
    data = request.get_json()
    query = data.get("product_name", "").strip()

    if not query:
        return jsonify({"error": "Missing 'product_name'"}), 400

    related = complement_map.get(query, [])
    return jsonify({
        "query": query,
        "complementary_products": related
    })



if __name__ == '__main__':
    app.run(debug=True)
