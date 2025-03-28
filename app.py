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
    
    pdf.cell(120, 7, "Total Before Tax:", align='L')
    pdf.cell(70, 7, f"{total_amount:.2f}", align='R', ln=True)
    pdf.cell(120, 7, f"CGST ({cgst}%):", align='L')
    pdf.cell(70, 7, f"{cgst_amount:.2f}", align='R', ln=True)
    pdf.cell(120, 7, f"SGST ({sgst}%):", align='L')
    pdf.cell(70, 7, f"{sgst_amount:.2f}", align='R', ln=True)
    pdf.cell(120, 7, f"IGST ({igst}%):", align='L')
    pdf.cell(70, 7, f"{igst_amount:.2f}", align='R', ln=True)
    pdf.cell(120, 7, "Total After Tax:", align='L')
    pdf.cell(70, 7, f"{total_after_tax:.2f}", align='R', ln=True)
    pdf.cell(190, 7, f"Total in Words: {num2words(total_after_tax, to='currency', lang='en')} only", ln=True)
    
    pdf.ln(10)
    pdf.cell(190, 7, "E-Way Bill No: {eway_bill}", ln=True)
    pdf.ln(5)
    pdf.cell(190, 7, "Bank Details: Priti Enterprises", ln=True)
    pdf.cell(190, 7, "Bank Name: Punjab National Bank", ln=True)
    pdf.cell(190, 7, "A/c No.: 005308700006153", ln=True)
    pdf.cell(190, 7, "IFSC Code: PUNB0005300", ln=True)
    pdf.cell(190, 7, "GST Payable on Reverse Charge: No", ln=True)
    
    pdf.ln(15)
    pdf.cell(95, 7, "Authorized Signature", ln=True, align='L')
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f"invoice_{invoice_no}.pdf")
    pdf.output(temp_file.name)
    return temp_file.name
