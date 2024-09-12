# Payment App 

## Overview

This is a Streamlit-based web application for handling payment transactions using UPI (Unified Payments Interface). The app provides three key functionalities:

1. **Generate Payment QR Code**: Create a UPI payment QR code for a specified amount.
2. **Upload Payment Screenshot**: Upload a payment screenshot, extract the UPI reference number (UTR), and check the transaction status.
3. **View Transactions**: Fetch and display a paginated list of transactions from the server.

---

## Features

1. **Generate Payment QR Code**:  
   Users can input the amount, and the app will generate a UPI QR code. This QR code can be scanned to make payments directly through UPI.

2. **Upload Payment Screenshot**:  
   Users can upload a screenshot of the payment receipt, and the app will extract the UPI reference (UTR) from the image using OCR (Tesseract). It then checks the transaction status against a server using this UPI reference.

3. **View Transactions**:  
   Users can fetch and view a paginated list of all transactions, displaying the details of each one.

---

## Setup and Configuration

### Environment Variables

Create a `.env` file in the project root or use `config.env`. Define the following variables:

```bash
SERVER_URL=http://localhost:5000    # API endpoint for transaction data (assumed to be available on a separate server)
UPI_ID=abc@ybl            # UPI ID for generating payment QR codes
DOWNLOADS_DIR=downloads             # Directory to store generated QR codes
```

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kevinnadar22/UPI.Payment.Gateway --branch demo-web upi-payment-app
   cd upi-payment-app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR** (required for extracting UPI ref number from images):
   - Ubuntu:
     ```bash
     sudo apt-get install tesseract-ocr
     ```
   - macOS:
     ```bash
     brew install tesseract
     ```
   - Windows: [Download the installer](https://github.com/tesseract-ocr/tesseract/wiki)

### Running the App

```bash
streamlit run app.py
```

The app will be accessible at `http://localhost:8501`.

---

## How to Use

### 1. Generate Payment QR Code
- Enter an amount.
- Click on **Generate QR Code**.
- The app will display the generated QR code.
- You can download the QR code as a PNG image.

### 2. Upload Payment Screenshot
- Upload a screenshot of the payment receipt (supported formats: PNG, JPG, JPEG).
- The app will extract the UPI reference number and fetch the transaction details from the server.

### 3. View Transactions
- Enter the page number and select the number of transactions per page.
- Click on **Fetch Transactions** to view the list of transactions.

---

## Technologies Used

- **Streamlit**: For building the web application interface.
- **QRCode**: For generating QR codes.
- **PIL (Python Imaging Library)**: For handling images.
- **Tesseract**: For OCR (Optical Character Recognition) to extract text from images.
- **Flask**: (Backend API to serve transaction data) *Not included in this app, assumed to be available on a separate server*.

---

## License

This project is licensed under the MIT License.