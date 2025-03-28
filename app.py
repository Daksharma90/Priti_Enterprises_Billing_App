import streamlit as st
from fpdf import FPDF
import datetime
from num2words import num2words  # Added for amount in words

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
    pdf.cell(100, 6, f"GSTIN: {data['billed_to_gstin']}")
    pdf.cell(100, 6, f"GSTIN: {data['shipped_to_gstin']}", ln=True)
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
        amount = round(product['qty'] * product['rate'], 2)
        total += amount
        pdf.cell(10, 6, str(i+1), border=1)
        pdf.cell(80, 6, product['name'], border=1)
        pdf.cell(20, 6, product['hsn_sac'], border=1)
        pdf.cell(15, 6, str(product['qty']), border=1)
        pdf.cell(20, 6, f"{product['rate']:.2f}", border=1)
        pdf.cell(30, 6, f"{amount:.2f}", border=1, ln=True)
    
    pdf.ln(5)

    # Tax Calculation (User Input)
    cgst_rate = data['cgst_rate'] / 100
    sgst_rate = data['sgst_rate'] / 100
    igst_rate = data['igst_rate'] / 100

    cgst = round(total * cgst_rate, 2)
    sgst = round(total * sgst_rate, 2)
    igst = round(total * igst_rate, 2)
    
    total_after_tax = round(total + cgst + sgst + igst, 2)

    # Convert total amount to words
    total_in_words = num2words(total_after_tax, lang='en').capitalize() + " only"

    # Right-Aligned Totals
    pdf.cell(145, 6, "Total Amount Before Tax:", border=0, align='R')
    pdf.cell(30, 6, f"{total:.2f}", border=1, ln=True)
    
    pdf.cell(145, 6, f"CGST ({data['cgst_rate']}%):", border=0, align='R')
    pdf.cell(30, 6, f"{cgst:.2f}", border=1, ln=True)
    
    pdf.cell(145, 6, f"SGST ({data['sgst_rate']}%):", border=0, align='R')
    pdf.cell(30, 6, f"{sgst:.2f}", border=1, ln=True)

    pdf.cell(145, 6, f"IGST ({data['igst_rate']}%):", border=0, align='R')
    pdf.cell(30, 6, f"{igst:.2f}", border=1, ln=True)
    
    pdf.cell(145, 6, "Total Amount After Tax:", border=0, align='R')
    pdf.cell(30, 6, f"{total_after_tax:.2f}", border=1, ln=True)
    
    # Display total amount in words
    pdf.ln(5)
    pdf.cell(200, 6, f"Total Amount (In Words): {total_in_words}", ln=True)

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

# Tax Input
cgst_rate = st.number_input("CGST Rate (%)", min_value=0.0, step=0.1, value=9.0)
sgst_rate = st.number_input("SGST Rate (%)", min_value=0.0, step=0.1, value=9.0)
igst_rate = st.number_input("IGST Rate (%)", min_value=0.0, step=0.1, value=0.0)

# Product Details
st.subheader("Products / Services")
products = []
n = st.number_input("Number of Products", min_value=1, step=1)
for i in range(n):
    name = st.text_input(f"Product {i+1} Name", key=f"name_{i}")
    hsn_sac = st.text_input(f"Product {i+1} HSN/SAC Code", key=f"hsn_{i}")
    qty = st.number_input(f"Product {i+1} Quantity", min_value=1, key=f"qty_{i}")
    rate = st.number_input(f"Product {i+1} Rate", min_value=0.0, format="%.2f", key=f"rate_{i}")
    products.append({"name": name, "hsn_sac": hsn_sac, "qty": qty, "rate": rate})

if st.button("Generate Invoice"):
    invoice_data = {"invoice_no": invoice_no, "invoice_date": invoice_date, "reverse_charge": reverse_charge, 
                    "products": products, "cgst_rate": cgst_rate, "sgst_rate": sgst_rate, "igst_rate": igst_rate}
    pdf = generate_invoice(invoice_data)
    st.download_button("Download Invoice", pdf, "invoice.pdf", "application/pdf")
