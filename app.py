import streamlit as st
from fpdf import FPDF
import tempfile
import os
from num2words import num2words
import datetime

def generate_invoice(invoice_no, invoice_date, customer_name, address, gstin, state, transport_mode, vehicle_no, eway_bill, items, cgst, sgst, igst):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
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
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(190, 7, "Details of Receiver / Billed to:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(190, 7, f"Name: {customer_name}", ln=True)
    pdf.cell(190, 7, f"Address: {address}", ln=True)
    pdf.cell(190, 7, f"GSTIN: {gstin}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(190, 7, "Ship To:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(190, 7, f"Name: {customer_name}", ln=True)
    pdf.cell(190, 7, f"Address: {address}", ln=True)
    pdf.cell(190, 7, f"GSTIN: {gstin}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(10, 8, "S.No", border=1, align='C')
    pdf.cell(50, 8, "Product Name", border=1, align='C')
    pdf.cell(20, 8, "HSN/SAC", border=1, align='C')
    pdf.cell(15, 8, "Qty", border=1, align='C')
    pdf.cell(20, 8, "Rate", border=1, align='C')
    pdf.cell(25, 8, "Amount", border=1, align='C')
    pdf.cell(25, 8, "GST Payable RCM", border=1, align='C')
    pdf.ln()
    
    total_amount = 0
    for i, item in enumerate(items, 1):
        name, hsn, qty, rate = item
        amount = int(qty) * float(rate)
        total_amount += amount
        pdf.cell(10, 8, str(i), border=1, align='C')
        pdf.cell(50, 8, name, border=1, align='L')
        pdf.cell(20, 8, hsn, border=1, align='C')
        pdf.cell(15, 8, str(qty), border=1, align='C')
        pdf.cell(20, 8, str(rate), border=1, align='C')
        pdf.cell(25, 8, str(amount), border=1, align='C')
        pdf.cell(25, 8, "No", border=1, align='C')
        pdf.ln()
    
    pdf.ln(5)
    cgst_amount = (total_amount * cgst) / 100
    sgst_amount = (total_amount * sgst) / 100
    igst_amount = (total_amount * igst) / 100
    total_after_tax = total_amount + cgst_amount + sgst_amount + igst_amount
    
    pdf.cell(120, 7, "Total Before Tax:", align='L')
    pdf.cell(70, 7, f"{total_amount:.2f}", align='R', ln=True)
    pdf.cell(120, 7, f"CGST ({cgst}%):", align='L')
    pdf.cell(70, 7, f"{cgst_amount:.2f}", align='R', ln=True)
    pdf.cell(120, 7, f"SGST ({sgst}%):", align='L')
    pdf.cell(70, 7, f"{sgst_amount:.2f}", align='R', ln=True)
    pdf.cell(120, 7, f"IGST ({igst}%):", align='L')
    pdf.cell(70, 7, f"{igst_amount:.2f}", align='R', ln=True)
    pdf.cell(190, 7, f"Total in Words: {num2words(total_after_tax, lang='en_IN')} Rupees only", ln=True)
    
    pdf.ln(10)
    pdf.cell(190, 7, f"E-Way Bill No: {eway_bill}", ln=True)
    pdf.ln(5)
    pdf.cell(190, 7, "Bank Details: Punjab National Bank", ln=True)
    pdf.cell(190, 7, "A/c No.: 005308700006153", ln=True)
    pdf.cell(190, 7, "IFSC Code: PUNB0005300", ln=True)
    pdf.ln(10)
    pdf.cell(95, 7, "Authorized Signature", ln=True, align='L')
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

st.title("Invoice Generator")
invoice_no = st.text_input("Invoice No")
invoice_date = st.date_input("Invoice Date", datetime.date.today())
customer_name = st.text_input("Customer Name")
address = st.text_area("Customer Address")
gstin = st.text_input("GSTIN")
state = st.text_input("State")
transport_mode = st.text_input("Transport Mode")
vehicle_no = st.text_input("Vehicle No")
eway_bill = st.text_input("E-Way Bill No")
cgst = st.number_input("CGST (%)", min_value=0.0)
sgst = st.number_input("SGST (%)", min_value=0.0)
igst = st.number_input("IGST (%)", min_value=0.0)

if st.button("Generate Invoice"):
    pdf_path = generate_invoice(invoice_no, invoice_date, customer_name, address, gstin, state, transport_mode, vehicle_no, eway_bill, [], cgst, sgst, igst)
    with open(pdf_path, "rb") as file:
        st.download_button("Download Invoice", file, file_name="invoice.pdf")
