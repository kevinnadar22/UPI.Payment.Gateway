import traceback
from flask import Flask, request, jsonify
import re
from pymongo import MongoClient
from datetime import datetime
from config import Config, TransactionType

# Initialize Flask app
app = Flask(__name__)

# MongoDB setup
client = MongoClient(Config.DATABASE_URL)
db = client[Config.DATABASE_NAME]
collection = db["transactions"]

# Regex patterns
amount_pattern = re.compile(r"(\d{1,3}(,\d{3})*|\d+)\.\d{2}")
upi_ref_pattern = re.compile(r"(\d{12})")  # 12 digit UPI reference pattern
upi_id_pattern = re.compile(r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}")  # UPI ID pattern
transaction_type_pattern = re.compile(r"credited|debited", re.IGNORECASE)


@app.route("/")
def index():
    return jsonify({"message": "ok"}), 200


@app.route("/transaction", methods=["POST"])
def parse_transaction():
    """Parses the transaction message and stores it in the database."""
    try:
        if request.content_type == "application/json":
            message = request.json.get("message", "")
        elif "application/x-www-form-urlencoded" in request.content_type:
            message = request.form.get("message", "")
        else:
            return jsonify({"error": "Invalid content type"}), 400

        # Extract transaction details
        amount_match = amount_pattern.search(message)
        upi_ref_match = upi_ref_pattern.search(message)
        transaction_type_match = transaction_type_pattern.search(message).group(0).lower()

        credited_match = transaction_type_match == TransactionType.CREDITED.value
        debited_match = transaction_type_match == TransactionType.DEBITED.value
        upi_id_match = upi_id_pattern.search(message)

        if not (amount_match and upi_ref_match and (credited_match or debited_match)):
            return jsonify({"error": "Invalid message format"}), 400

        # Clean extracted values
        amount = float(amount_match.group(0).replace(",", "").replace(" ", ""))
        upi_ref = int(upi_ref_match.group(1))
        upi_id = upi_id_match.group(0) if upi_id_match else None

        # Check if transaction already exists
        if db.transactions.find_one({"upi_ref": upi_ref}):
            return jsonify({"error": "Transaction already recorded"}), 400

        # Create transaction record
        transaction = {
            "amount": amount,
            "upi_ref": upi_ref,
            "upi_id": upi_id,
            "credited": credited_match,
            "debited": debited_match,
            "message": message,
            "timestamp": datetime.now(),
        }
        # Insert transaction into MongoDB
        collection.insert_one(transaction)

        return jsonify({"message": "Transaction recorded successfully"}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/transaction/<upi_ref>", methods=["GET"])
def get_transaction(upi_ref):
    """Fetches a transaction by UPI reference number."""
    try:
        if not upi_ref.isdigit():
            return jsonify({"error": "Invalid UPI Red"}), 400 
        upi_ref = int(upi_ref)
        transaction = db.transactions.find_one({"upi_ref": upi_ref})
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404
        transaction.pop("_id")
        return jsonify(transaction), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/transaction", methods=["GET"])
def get_all_transactions():
    """Fetches all transactions with pagination support."""
    try:
        # Pagination query parameters
        page = int(request.args.get("page", 1))  # Default page = 1
        per_page = int(request.args.get("per_page", 10))  # Default per page = 10

        # Calculate offset for pagination
        skip = (page - 1) * per_page

        # Fetch transactions with pagination
        transactions = list(collection.find().skip(skip).limit(per_page))

        # Get total transaction count
        total_transactions = collection.count_documents({})

        # Remove MongoDB ObjectID from response
        for transaction in transactions:
            transaction.pop("_id")

        # Prepare paginated response
        response = {
            "transactions": transactions,
            "page": page,
            "per_page": per_page,
            "total_transactions": total_transactions,
            "total_pages": (total_transactions + per_page - 1) // per_page,
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
