import streamlit as st
from fpdf import FPDF
import tempfile
import os
from num2words import num2words
import datetime

def generate_invoice(invoice_no, invoice_date, customer_name, address, gstin, state, transport_mode, vehicle_no, eway_bill, items, cgst, sgst, igst):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "PRITI ENTERPRISES", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(190, 7, "Near Santu Tubwel, Tosham Road Bypass, Bhiwani - 127021 (Haryana)", ln=True, align='C')
    pdf.cell(190, 7, "GSTIN: 06APGPK2323H1Z8", ln=True, align='C')
    pdf.ln(8)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(95, 8, f"Invoice No: {invoice_no}")
    pdf.cell(95, 8, f"Invoice Date: {invoice_date}", ln=True)
    pdf.cell(95, 8, f"State: {state} (State Code: 06)", ln=True)
    pdf.cell(95, 8, f"Transport Mode: {transport_mode}")
    pdf.cell(95, 8, f"Vehicle No: {vehicle_no}", ln=True)
    pdf.cell(95, 8, f"E-Way Bill No: {eway_bill}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(190, 7, "Details of Receiver / Billed to:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(190, 7, f"Name: {customer_name}", ln=True)
    pdf.cell(190, 7, f"Address: {address}", ln=True)
    pdf.cell(190, 7, f"GSTIN: {gstin}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(10, 8, "S.No", border=1, align='C')
    pdf.cell(60, 8, "Product Name", border=1, align='C')
    pdf.cell(25, 8, "HSN/SAC", border=1, align='C')
    pdf.cell(20, 8, "Qty", border=1, align='C')
    pdf.cell(25, 8, "Rate", border=1, align='C')
    pdf.cell(30, 8, "Amount", border=1, align='C')
    pdf.ln()
    
    total_amount = 0
    for i, item in enumerate(items, 1):
        name, hsn, qty, rate = item
        amount = int(qty) * float(rate)
        total_amount += amount
        pdf.cell(10, 8, str(i), border=1, align='C')
        pdf.cell(60, 8, name, border=1, align='L')
        pdf.cell(25, 8, hsn, border=1, align='C')
        pdf.cell(20, 8, str(qty), border=1, align='C')
        pdf.cell(25, 8, str(rate), border=1, align='C')
        pdf.cell(30, 8, str(amount), border=1, align='C')
        pdf.ln()
    
    pdf.ln(5)
    cgst_amount = (total_amount * cgst) / 100
    sgst_amount = (total_amount * sgst) / 100
    igst_amount = (total_amount * igst) / 100
    total_after_tax = total_amount + cgst_amount + sgst_amount + igst_amount
    
    pdf.cell(190, 7, f"Total Before Tax: {total_amount:.2f}", ln=True)
    pdf.cell(190, 7, f"CGST ({cgst}%): {cgst_amount:.2f}", ln=True)
    pdf.cell(190, 7, f"SGST ({sgst}%): {sgst_amount:.2f}", ln=True)
    pdf.cell(190, 7, f"IGST ({igst}%): {igst_amount:.2f}", ln=True)
    pdf.cell(190, 7, f"Total After Tax: {total_after_tax:.2f}", ln=True)
    pdf.cell(190, 7, f"Total in Words: {num2words(total_after_tax, to='currency', lang='en_IN')} only", ln=True)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

st.title("Billing App - Priti Enterprises")

invoice_no = st.text_input("Invoice Number")
invoice_date = st.date_input("Invoice Date", value=datetime.date.today())
customer_name = st.text_input("Customer Name")
address = st.text_area("Customer Address")
gstin = st.text_input("GSTIN")
state = st.text_input("State")
transport_mode = st.text_input("Transport Mode")
vehicle_no = st.text_input("Vehicle Number")
eway_bill = st.text_input("E-Way Bill Number")
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
        pdf_path = generate_invoice(invoice_no, invoice_date, customer_name, address, gstin, state, transport_mode, vehicle_no, eway_bill, items, cgst, sgst, igst)
        with open(pdf_path, "rb") as file:
            st.download_button("Download Invoice", file, file_name="invoice.pdf", mime="application/pdf")
        os.unlink(pdf_path)
    else:
        st.error("Please fill all fields.")
