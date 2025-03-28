import streamlit as st
from fpdf import FPDF
import tempfile
import os
from num2words import num2words
import datetime

def generate_invoice(invoice_no, invoice_date, receiver_name, receiver_address, receiver_gstin, receiver_state,
                      consignee_name, consignee_address, consignee_gstin, consignee_state, transport_mode, vehicle_no,
                      date_of_supply, place_of_supply, items, cgst, sgst, igst):
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
    pdf.cell(95, 8, f"State: Haryana (State Code: 06)")
    pdf.cell(95, 8, f"Date of Supply: {date_of_supply}", ln=True)
    pdf.cell(95, 8, f"Place of Supply: {place_of_supply}", ln=True)
    pdf.cell(95, 8, f"Transport Mode: {transport_mode}")
    pdf.cell(95, 8, f"Vehicle No: {vehicle_no}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(95, 7, "Details of Receiver | Billed to:")
    pdf.cell(95, 7, "Details of Consignee | Shipped to:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(95, 7, f"Name: {receiver_name}")
    pdf.cell(95, 7, f"Name: {consignee_name}", ln=True)
    pdf.cell(95, 7, f"Address: {receiver_address}")
    pdf.cell(95, 7, f"Address: {consignee_address}", ln=True)
    pdf.cell(95, 7, f"GSTIN: {receiver_gstin}")
    pdf.cell(95, 7, f"GSTIN: {consignee_gstin}", ln=True)
    pdf.cell(95, 7, f"State: {receiver_state}")
    pdf.cell(95, 7, f"State: {consignee_state}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(10, 8, "Sr. No", border=1, align='C')
    pdf.cell(60, 8, "Name of Product / Service", border=1, align='C')
    pdf.cell(20, 8, "HSN/SAC", border=1, align='C')
    pdf.cell(15, 8, "Qty", border=1, align='C')
    pdf.cell(25, 8, "Rate", border=1, align='C')
    pdf.cell(25, 8, "Amount", border=1, align='C')
    pdf.ln()
    
    total_amount = 0
    for i, item in enumerate(items, 1):
        name, hsn, qty, rate = item
        amount = int(qty) * float(rate)
        total_amount += amount
        pdf.cell(10, 8, str(i), border=1, align='C')
        pdf.cell(60, 8, name, border=1, align='L')
        pdf.cell(20, 8, hsn, border=1, align='C')
        pdf.cell(15, 8, str(qty), border=1, align='C')
        pdf.cell(25, 8, str(rate), border=1, align='C')
        pdf.cell(25, 8, str(amount), border=1, align='C')
        pdf.ln()
    
    pdf.ln(5)
    pdf.cell(120, 7, "Total Before Tax:", align='L')
    pdf.cell(70, 7, f"{total_amount:.2f}", align='R', ln=True)
    pdf.cell(120, 7, f"CGST ({cgst}%):", align='L')
    pdf.cell(70, 7, f"{(total_amount * cgst) / 100:.2f}", align='R', ln=True)
    pdf.cell(120, 7, f"SGST ({sgst}%):", align='L')
    pdf.cell(70, 7, f"{(total_amount * sgst) / 100:.2f}", align='R', ln=True)
    pdf.cell(120, 7, f"IGST ({igst}%):", align='L')
    pdf.cell(70, 7, f"{(total_amount * igst) / 100:.2f}", align='R', ln=True)
    pdf.cell(120, 7, "Grand Total (in words):", align='L')
    pdf.multi_cell(70, 7, num2words(total_amount, lang='en').title() + " Only", align='R')
    
    pdf.ln(10)
    pdf.cell(190, 7, "Bank Details: Punjab National Bank", ln=True)
    pdf.cell(190, 7, "A/c No.: 005308700006153", ln=True)
    pdf.cell(190, 7, "IFSC Code: PUNB0005300", ln=True)
    pdf.ln(10)
    pdf.cell(190, 7, "Terms & Conditions:", ln=True)
    pdf.cell(190, 7, "1. Goods once sold will not be taken back.", ln=True)
    pdf.cell(190, 7, "2. Interest @ 18% p.a. will be charged if payment is not made in time.", ln=True)
    pdf.cell(190, 7, "3. Subject to Bhiwani Jurisdiction Only.", ln=True)
    pdf.ln(10)
    pdf.cell(95, 7, "Authorized Signature", ln=True, align='L')
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

st.title("Invoice Generator")

invoice_no = st.text_input("Invoice No", "249")
invoice_date = st.date_input("Invoice Date", datetime.date.today())
receiver_name = st.text_input("Receiver Name", "Receiver Name")
receiver_address = st.text_area("Receiver Address", "Receiver Address")
receiver_gstin = st.text_input("Receiver GSTIN", "1234567890")
consignee_name = st.text_input("Consignee Name", "Consignee Name")
consignee_address = st.text_area("Consignee Address", "Consignee Address")
consignee_gstin = st.text_input("Consignee GSTIN", "0987654321")
transport_mode = st.text_input("Transport Mode", "Road")
vehicle_no = st.text_input("Vehicle No", "HR-1234")
date_of_supply = st.date_input("Date of Supply", datetime.date.today())
place_of_supply = st.text_input("Place of Supply", "Bhiwani")
cgst = st.number_input("CGST (%)", 0, 100, 9)
sgst = st.number_input("SGST (%)", 0, 100, 9)
igst = st.number_input("IGST (%)", 0, 100, 18)

if st.button("Generate Invoice"):
    pdf_file = generate_invoice(invoice_no, invoice_date, receiver_name, receiver_address, receiver_gstin,
                                receiver_state, consignee_name, consignee_address, consignee_gstin, consignee_state,
                                transport_mode, vehicle_no, date_of_supply, place_of_supply, [], cgst, sgst, igst)

    with open(pdf_file, "rb") as file:
        st.download_button(label="Download Invoice", data=file, file_name="invoice.pdf", mime="application/pdf")
