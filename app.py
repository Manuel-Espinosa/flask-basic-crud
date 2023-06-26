from flask import Flask, request, jsonify, make_response
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27018/storedb"
mongo = PyMongo(app)
db = mongo.db.products

@app.route('/', methods=['GET'])
def index():
    return "<h1>Hello World!</h1>"

@app.route('/products', methods=['POST'])
def createProduct():
    product = db.insert_one({
        "title": request.json["title"],
        "price": request.json["price"],
        "category": request.json["category"],
        "description": request.json["description"],
        "image": request.json["image"]
    })

    response = make_response(
        jsonify({
            'id': str(product.inserted_id)
        }),
        201
    )
    response.headers['Content-type'] = 'application/json'
    return response

@app.route('/products', methods=['GET'])
def getAllProducts():
    products = db.find()
    result = []
    for product in products:
        result.append({
            "id": str(product["_id"]),
            "title": product["title"],
            "price": product["price"],
            "category": product["category"],
            "description": product["description"],
            "image": product["image"]
        })
    return jsonify(result)

@app.route("/product/<id>", methods=["GET"])
def getProduct(id):
    product = db.find_one({
        "_id": ObjectId(id)
    })

    if product:
        return jsonify({
            "_id": str(ObjectId(product["_id"])),
            "title": product["title"],
            "price": product["price"],
            "category": product["category"],
            "description": product["description"],
            "image": product["image"]
        })
    else:
        return jsonify({"message": "Product not found."}), 404

@app.route("/product/<id>", methods=["PUT"])
def updateProduct(id):
    product = db.find_one({
        "_id": ObjectId(id)
    })

    if product:
        db.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "title": request.json.get("title", product["title"]),
                "price": request.json.get("price", product["price"]),
                "category": request.json.get("category", product["category"]),
                "description": request.json.get("description", product["description"]),
                "image": request.json.get("image", product["image"])
            }}
        )
        return jsonify({"message": "Product updated successfully."}), 200
    else:
        return jsonify({"message": "Product not found."}), 404

@app.route("/product/<id>", methods=["DELETE"])
def deleteProduct(id):
    product = db.find_one({
        "_id": ObjectId(id)
    })

    if product:
        db.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "Product deleted successfully."}), 200
    else:
        return jsonify({"message": "Product not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
