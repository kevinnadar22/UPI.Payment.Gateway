from flask import Flask, request, jsonify
import re
from pymongo import MongoClient
from datetime import datetime
from config import Config, TransactionType

app = Flask(__name__)

# MongoDB setup
client = MongoClient(Config.DATABASE_URL)
db = client[Config.DATABASE_NAME]
collection = db["transactions"]

# Regex patterns
amount_pattern = re.compile(r"(\d{1,3}(,\d{3})*|\d+)(\.\d{2})?")
# 12 digit number pattern
upi_ref_pattern = re.compile(r"(\d{12})")
credited_pattern = re.compile(rf"{TransactionType.CREDITED.value}")
debited_pattern = re.compile(rf"{TransactionType.DEBITED.value}")
upi_id_pattern = re.compile(r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}")


@app.route("/")
def index():
    return jsonify({"message": "ok"})


@app.route("/transaction", methods=["POST"])
def parse_transaction():
    try:
        message = request.json.get("message", "")

        # Extracting details
        amount_match = amount_pattern.search(message)
        upi_ref_match = upi_ref_pattern.search(message)
        credited_match = credited_pattern.search(message)
        debited_match = debited_pattern.search(message)
        upi_id_match = upi_id_pattern.search(message)

        if not (amount_match and upi_ref_match and (credited_match or debited_match)):
            return jsonify({"error": "Invalid message format"}), 400

        amount = float(amount_match.group(0).replace(",", "").replace(" ", ""))
        upi_ref = upi_ref_match.group(1)
        transaction_type = "credited" if credited_match else "debited"
        if upi_id_match:
            upi_id = upi_id_match.group(0)
        else:
            upi_id = None

        if db.transactions.find_one({"upi_ref": upi_ref}):
            return jsonify({"error": "Transaction already recorded"}), 400

        transaction = {
            "amount": amount,
            "upi_ref": upi_ref,
            "upi_id": upi_id,
            "transaction_type": transaction_type,
            "timestamp": datetime.now(),
            "message": message,
        }

        # Inserting into MongoDB
        collection.insert_one(transaction)

        return jsonify({"message": "Transaction recorded successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host=Config.HOST, port=Config.PORT)
