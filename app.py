import streamlit as st
from fpdf import FPDF
import tempfile
import os
from num2words import num2words

def generate_invoice(invoice_no, customer_name, address, gstin, state, items, cgst, sgst, igst):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "PRITI ENTERPRISES", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Near Santu Tubwel, Tosham Road Bypass, Bhiwani - 127021 (Haryana)", ln=True, align='C')
    pdf.cell(200, 10, "GSTIN: 06APGPK2323H1Z8", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, f"Invoice No: {invoice_no}")
    pdf.cell(100, 10, f"Invoice Date: {st.session_state['invoice_date']}", ln=True)
    pdf.cell(100, 10, f"State: {state} (State Code: 06)", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, "Details of Receiver / Billed to:")
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Name: {customer_name}", ln=True)
    pdf.cell(200, 10, f"Address: {address}", ln=True)
    pdf.cell(200, 10, f"GSTIN: {gstin}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(10, 10, "S.No", border=1)
    pdf.cell(50, 10, "Product Name", border=1)
    pdf.cell(30, 10, "HSN/SAC", border=1)
    pdf.cell(20, 10, "Qty", border=1)
    pdf.cell(30, 10, "Rate", border=1)
    pdf.cell(30, 10, "Amount", border=1)
    pdf.cell(30, 10, "Taxable Value", border=1)
    pdf.ln()
    
    total_amount = 0
    for i, item in enumerate(items, 1):
        name, hsn, qty, rate = item
        amount = int(qty) * float(rate)
        total_amount += amount
        pdf.cell(10, 10, str(i), border=1)
        pdf.cell(50, 10, name, border=1)
        pdf.cell(30, 10, hsn, border=1)
        pdf.cell(20, 10, str(qty), border=1)
        pdf.cell(30, 10, str(rate), border=1)
        pdf.cell(30, 10, str(amount), border=1)
        pdf.cell(30, 10, str(amount), border=1)
        pdf.ln()
    
    pdf.ln(5)
    cgst_amount = (total_amount * cgst) / 100
    sgst_amount = (total_amount * sgst) / 100
    igst_amount = (total_amount * igst) / 100
    total_after_tax = total_amount + cgst_amount + sgst_amount + igst_amount
    
    pdf.cell(200, 10, f"Total Before Tax: {total_amount}", ln=True)
    pdf.cell(200, 10, f"CGST ({cgst}%): {cgst_amount}", ln=True)
    pdf.cell(200, 10, f"SGST ({sgst}%): {sgst_amount}", ln=True)
    pdf.cell(200, 10, f"IGST ({igst}%): {igst_amount}", ln=True)
    pdf.cell(200, 10, f"Total After Tax: {total_after_tax}", ln=True)
    pdf.cell(200, 10, f"Total in Words: {num2words(total_after_tax).capitalize()} only", ln=True)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

st.title("Billing App - Priti Enterprises")

invoice_no = st.text_input("Invoice Number")
st.session_state['invoice_date'] = st.date_input("Invoice Date")
customer_name = st.text_input("Customer Name")
address = st.text_area("Customer Address")
gstin = st.text_input("GSTIN")
state = st.text_input("State")
cgst = st.number_input("CGST (%)", min_value=0.0, step=0.1)
sgst = st.number_input("SGST (%)", min_value=0.0, step=0.1)
igst = st.number_input("IGST (%)", min_value=0.0, step=0.1)

items = []
num_items = st.number_input("Number of Items", min_value=1, step=1, value=1)

for i in range(num_items):
    st.subheader(f"Item {i+1}")
    name = st.text_input(f"Item {i+1} Name", key=f"name_{i}")
    hsn = st.text_input(f"Item {i+1} HSN/SAC", key=f"hsn_{i}")
    qty = st.number_input(f"Item {i+1} Quantity", min_value=1, step=1, key=f"qty_{i}")
    rate = st.number_input(f"Item {i+1} Rate", min_value=0.0, step=0.01, key=f"rate_{i}")
    items.append((name, hsn, qty, rate))

if st.button("Generate Invoice"):
    if customer_name and all(item[0] for item in items):
        pdf_path = generate_invoice(invoice_no, customer_name, address, gstin, state, items, cgst, sgst, igst)
        with open(pdf_path, "rb") as file:
            st.download_button("Download Invoice", file, file_name="invoice.pdf", mime="application/pdf")
        os.unlink(pdf_path)
    else:
        st.error("Please fill all fields.")
