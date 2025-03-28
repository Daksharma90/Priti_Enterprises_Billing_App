import streamlit as st
from fpdf import FPDF
import datetime

def generate_invoice(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    
    # Header
    pdf.cell(200, 10, "PRITI ENTERPRISES", ln=True, align='C')
    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 5, "Near Santu Tubwel, Tosham Road Baypass, Bhiwani - 127021 (Haryana)", ln=True, align='C')
    pdf.ln(5)
    
    # Invoice Details
    pdf.cell(100, 6, f"Invoice No: {data['invoice_no']}")
    pdf.cell(100, 6, f"Invoice Date: {data['invoice_date']}", ln=True)
    pdf.cell(100, 6, f"State: Haryana  State Code: 06")
    pdf.cell(100, 6, f"Reverse Charge: {data['reverse_charge']}", ln=True)
    pdf.ln(5)
    
    # Billed To
    pdf.set_font("Arial", "B", 10)
    pdf.cell(100, 6, "Billed To:")
    pdf.cell(100, 6, "Shipped To:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(100, 6, f"Name: {data['billed_to_name']}")
    pdf.cell(100, 6, f"Name: {data['shipped_to_name']}", ln=True)
    pdf.cell(100, 6, f"Address: {data['billed_to_address']}")
    pdf.cell(100, 6, f"Address: {data['shipped_to_address']}", ln=True)
    pdf.cell(100, 6, f"State: {data['billed_to_state']}")
    pdf.cell(100, 6, f"State: {data['shipped_to_state']}", ln=True)
    pdf.ln(5)
    
    # Table Header
    pdf.set_font("Arial", "B", 10)
    pdf.cell(10, 6, "Sr.", border=1)
    pdf.cell(80, 6, "Product / Service", border=1)
    pdf.cell(20, 6, "HSN/SAC", border=1)
    pdf.cell(15, 6, "Qty", border=1)
    pdf.cell(20, 6, "Rate", border=1)
    pdf.cell(30, 6, "Amount", border=1, ln=True)
    
    # Table Data
    pdf.set_font("Arial", "", 10)
    total = 0
    for i, product in enumerate(data['products']):
        pdf.cell(10, 6, str(i+1), border=1)
        pdf.cell(80, 6, product['name'], border=1)
        pdf.cell(20, 6, product['hsn_sac'], border=1)
        pdf.cell(15, 6, str(product['qty']), border=1)
        pdf.cell(20, 6, str(product['rate']), border=1)
        amount = product['qty'] * product['rate']
        total += amount
        pdf.cell(30, 6, str(amount), border=1, ln=True)
    
    pdf.ln(5)
    
    # Total Calculation
    pdf.cell(100, 6, "Total Amount Before Tax:")
    pdf.cell(50, 6, str(total), ln=True)
    pdf.cell(100, 6, "CGST (9%):")
    pdf.cell(50, 6, str(round(total * 0.09, 2)), ln=True)
    pdf.cell(100, 6, "SGST (9%):")
    pdf.cell(50, 6, str(round(total * 0.09, 2)), ln=True)
    pdf.cell(100, 6, "Total Amount After Tax:")
    pdf.cell(50, 6, str(round(total * 1.18, 2)), ln=True)
    
    pdf.ln(10)
    
    # Bank Details
    pdf.set_font("Arial", "B", 10)
    pdf.cell(200, 6, "Bank Details:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 6, "Bank Name: Punjab National Bank", ln=True)
    pdf.cell(200, 6, "Account No.: 005308700006153", ln=True)
    pdf.cell(200, 6, "IFSC Code: PUNB0005300", ln=True)
    pdf.ln(10)
    
    # Terms & Conditions
    pdf.set_font("Arial", "B", 10)
    pdf.cell(200, 6, "Terms & Conditions:", ln=True)
    pdf.set_font("Arial", "", 8)
    pdf.multi_cell(200, 5, "1. Goods once sold will not be taken back.\n2. Interest @18% p.a. will be charged if payment is not made in stipulated time.\n3. Subject to BHIWANI Jurisdiction Only.")
    
    pdf.ln(10)
    pdf.cell(200, 6, "For: PRITI ENTERPRISES", ln=True, align='R')
    pdf.cell(200, 6, "Authorized Signatory", ln=True, align='R')
    
    return pdf.output(dest='S').encode('latin1')

st.title("Invoice Generator")

# Invoice Details
invoice_no = st.text_input("Invoice No", "249")
invoice_date = st.date_input("Invoice Date", datetime.date.today()).strftime("%d-%m-%Y")
reverse_charge = st.selectbox("Reverse Charge", ["Y", "N"])

# Billed To
billed_to_name = st.text_input("Billed To - Name")
billed_to_address = st.text_area("Billed To - Address")
billed_to_state = st.text_input("Billed To - State")

# Shipped To
shipped_to_name = st.text_input("Shipped To - Name")
shipped_to_address = st.text_area("Shipped To - Address")
shipped_to_state = st.text_input("Shipped To - State")

# Product Details
st.subheader("Products / Services")
products = []
n = st.number_input("Number of Products", min_value=1, step=1)
for i in range(n):
    st.write(f"### Product {i+1}")
    name = st.text_input(f"Product {i+1} Name")
    hsn_sac = st.text_input(f"Product {i+1} HSN/SAC Code")
    qty = st.number_input(f"Product {i+1} Quantity", min_value=1)
    rate = st.number_input(f"Product {i+1} Rate", min_value=0.0, format="%.2f")
    products.append({"name": name, "hsn_sac": hsn_sac, "qty": qty, "rate": rate})

if st.button("Generate Invoice"):
    invoice_data = {
        "invoice_no": invoice_no,
        "invoice_date": invoice_date,
        "reverse_charge": reverse_charge,
        "billed_to_name": billed_to_name,
        "billed_to_address": billed_to_address,
        "billed_to_state": billed_to_state,
        "shipped_to_name": shipped_to_name,
        "shipped_to_address": shipped_to_address,
        "shipped_to_state": shipped_to_state,
        "products": products
    }
    pdf = generate_invoice(invoice_data)
    st.download_button("Download Invoice", pdf, "invoice.pdf", "application/pdf")
