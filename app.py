from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)

inventory = []
next_id = 1

@app.route("/")
def home():
    return "Welcome to the OpenFoodFacts Inventory API!"

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((item for item in inventory if item["id"] == item_id), None)
    if item is None:
        abort(404, description="Item not found")
    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def add_item():
    global next_id
    data = request.get_json()
    required_fields = ["product_name", "brands", "ingredients_text", "nutriscore"]
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required fields")

    item = {
        "id": next_id,
        "product_name": data["product_name"],
        "brands": data["brands"],
        "ingredients_text": data["ingredients_text"],
        "nutriscore": data["nutriscore"]
    }
    inventory.append(item)
    next_id += 1
    return jsonify(item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()
    item = next((item for item in inventory if item["id"] == item_id), None)
    if item is None:
        abort(404, description="Item not found")

    for field in ["product_name", "brands", "ingredients_text", "nutriscore"]:
        if field in data:
            item[field] = data[field]

    return jsonify(item), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global inventory
    item = next((item for item in inventory if item["id"] == item_id), None)
    if item is None:
        abort(404, description="Item not found")

    inventory = [i for i in inventory if i["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

def fetch_product_from_openfoodfacts(query):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": query,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        products = data.get("products", [])
        if not products:
            return None

        product = products[0]  # Take first product result
        return {
            "product_name": product.get("product_name", "Unknown"),
            "brands": product.get("brands", "Unknown"),
            "ingredients_text": product.get("ingredients_text", "Not available"),
            "nutriscore": product.get("nutriscore_grade", "N/A")
        }
    except Exception as e:
        print("Error fetching product:", e)
        return None

@app.route("/fetch-and-add", methods=["POST"])
def fetch_and_add():
    global next_id
    data = request.get_json()
    query = data.get("query")
    if not query:
        abort(400, description="Missing 'query' in request.")

    product = fetch_product_from_openfoodfacts(query)
    if not product:
        abort(404, description="No product found in OpenFoodFacts API.")

    product["id"] = next_id
    next_id += 1
    inventory.append(product)
    return jsonify(product), 201

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app.run(debug=True)
