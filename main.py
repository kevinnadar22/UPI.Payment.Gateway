import streamlit as st
import qrcode
from PIL import Image, ImageDraw
import pytesseract
import re
import os
import requests
from config import Config


# Helper functions
def get_utr_id_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        match = re.findall(r"\b\d(?:\s*\d){11}\b", text)
        if match:
            os.remove(image_path)
            return match
        else:
            return None
    except Exception as e:
        st.error(f"Error extracting UPI reference: {e}")
        return None


def create_payment_qr(price, upi_id=Config.UPI_ID):
    data = f"upi://pay?pa={upi_id}&pn=Channel%20Mart%20Admin&am={price}&tn=Pay%20And%20Contact%20the%20Owner&cu=INR"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = Image.new(
        "RGB",
        (qr.box_size * len(qr.get_matrix()), qr.box_size * len(qr.get_matrix())),
        "white",
    )
    draw = ImageDraw.Draw(qr_img)

    for r, row in enumerate(qr.get_matrix()):
        for c, val in enumerate(row):
            if val:
                draw.rectangle(
                    [
                        c * qr.box_size,
                        r * qr.box_size,
                        (c + 1) * qr.box_size,
                        (r + 1) * qr.box_size,
                    ],
                    fill="black",
                )

    return qr_img


def get_transactions(page, per_page):
    url = f"{Config.SERVER_URL}/transaction?page={page}&per_page={per_page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}


def get_transaction(upi_ref):
    upi_ref = upi_ref.replace(" ", "").strip()
    url = f"{Config.SERVER_URL}/transaction/{upi_ref}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}


# Streamlit App Layout
st.title("Payment App")

tab1, tab2, tab3 = st.tabs(["Home", "Upload Payment Screenshot", "View Transactions"])

# Tab 1: Generate Payment QR
with tab1:
    st.header("Generate Payment QR Code")
    amount = st.number_input("Enter amount", min_value=1.0, value=100.0)

    if st.button("Generate QR Code"):
        qr_image = create_payment_qr(amount)
        st.image(qr_image, caption="Payment QR Code", use_column_width=True)
        qr_image_path = f"{Config.DOWNLOADS_DIR}/payment_qr_{amount}.png"
        qr_image.save(qr_image_path)
        st.download_button(
            label="Download QR Code",
            data=qr_image_path,
            file_name=f"payment_qr_{amount}.png",
        )

# Tab 2: Upload Payment Screenshot
with tab2:
    st.header("Check Payment Status")
    uploaded_file = st.file_uploader(
        "Upload payment screenshot", type=["png", "jpg", "jpeg"]
    )
    utr_id = st.text_input("Enter UPI Reference")

    if uploaded_file or utr_id:

        if uploaded_file:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            image_path = f"uploaded_{uploaded_file.name}"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            utr_id = get_utr_id_from_image(image_path)
        else:
            utr_id = utr_id.split(",")

        for utr in utr_id:
            json_data = get_transaction(utr)
            if "error" not in json_data:
                break

        if "error" not in json_data:
            st.data_editor(json_data)
        elif json_data.get("error"):
            st.error(f"Error: {json_data['error']}")
        else:
            st.error("Unable to extract UPI Reference")

# Tab 3: View Transactions
with tab3:
    st.header("Transactions List")

    page = st.number_input("Page number", min_value=1, value=1)
    per_page = st.selectbox("Transactions per page", options=[5, 10, 20, 50], index=1)

    if st.button("Fetch Transactions"):
        transactions_data = get_transactions(page, per_page)

        if "error" not in transactions_data:
            transactions = transactions_data.get("transactions", [])
            total_pages = transactions_data.get("total_pages", 1)
            st.write(f"Showing page {page} of {total_pages}")
            transactions.reverse()
            st.data_editor(transactions)

        else:
            st.error(f"Error: {transactions_data['error']}")

os.makedirs(Config.DOWNLOADS_DIR, exist_ok=True)
