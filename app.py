import streamlit as st
from fpdf import FPDF
from datetime import datetime

def generate_invoice(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(200, 10, "PRITI ENTERPRISES", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 5, "Near Santu Tubwel, Tosham Road Baypass, Bhiwani - 127021 (Haryana)", ln=True, align='C')
    pdf.ln(5)
    
    # Invoice Details
    pdf.set_font("Arial", size=10)
    pdf.cell(100, 5, f"Invoice No: {data['invoice_no']}")
    pdf.cell(90, 5, f"Date: {data['invoice_date']}", ln=True)
    pdf.cell(100, 5, f"State: {data['state']}")
    pdf.cell(90, 5, f"State Code: {data['state_code']}", ln=True)
    pdf.ln(5)
    
    # Receiver and Consignee Details
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(95, 5, "Billed To:")
    pdf.cell(95, 5, "Shipped To:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(95, 5, data['billed_to'])
    pdf.cell(95, 5, data['shipped_to'], ln=True)
    pdf.cell(95, 5, f"GSTIN: {data['billed_gstin']}")
    pdf.cell(95, 5, f"GSTIN: {data['shipped_gstin']}", ln=True)
    pdf.ln(5)
    
    # Table Header
    pdf.set_font("Arial", style='B', size=10)
    pdf.cell(10, 5, "Sr.", border=1)
    pdf.cell(80, 5, "Product/Service", border=1)
    pdf.cell(20, 5, "HSN", border=1)
    pdf.cell(20, 5, "Qty", border=1)
    pdf.cell(30, 5, "Rate", border=1)
    pdf.cell(30, 5, "Amount", border=1, ln=True)
    pdf.set_font("Arial", size=10)
    
    total_amount = 0
    for i, item in enumerate(data['items']):
        pdf.cell(10, 5, str(i+1), border=1)
        pdf.cell(80, 5, item['name'], border=1)
        pdf.cell(20, 5, item['hsn'], border=1)
        pdf.cell(20, 5, str(item['qty']), border=1)
        pdf.cell(30, 5, f"{item['rate']:.2f}", border=1)
        amount = item['qty'] * item['rate']
        pdf.cell(30, 5, f"{amount:.2f}", border=1, ln=True)
        total_amount += amount
    
    pdf.ln(5)
    
    # Tax Calculation
    cgst = (data['cgst_rate'] / 100) * total_amount
    sgst = (data['sgst_rate'] / 100) * total_amount
    total_after_tax = total_amount + cgst + sgst
    
    pdf.cell(150, 5, "Total Amount Before Tax:")
    pdf.cell(40, 5, f"{total_amount:.2f}", ln=True)
    pdf.cell(150, 5, f"CGST ({data['cgst_rate']}%):")
    pdf.cell(40, 5, f"{cgst:.2f}", ln=True)
    pdf.cell(150, 5, f"SGST ({data['sgst_rate']}%):")
    pdf.cell(40, 5, f"{sgst:.2f}", ln=True)
    pdf.cell(150, 5, "Total Amount After Tax:")
    pdf.cell(40, 5, f"{total_after_tax:.2f}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 5, "TERMS & CONDITIONS:", ln=True)
    pdf.cell(200, 5, "1. Goods once sold will not be taken back.", ln=True)
    pdf.cell(200, 5, "2. Interest @ 18% p.a. will be charged if the payment is not made in time.", ln=True)
    pdf.output("invoice.pdf")
    return "invoice.pdf"

st.title("Invoice Generator - Priti Enterprises")

invoice_no = st.text_input("Invoice No", "249")
invoice_date = st.date_input("Invoice Date", datetime.today()).strftime('%d-%m-%Y')
state = st.text_input("State", "Haryana")
state_code = st.text_input("State Code", "06")

billed_to = st.text_input("Billed To")
billed_gstin = st.text_input("Billed GSTIN")
shipped_to = st.text_input("Shipped To")
shipped_gstin = st.text_input("Shipped GSTIN")

items = []
num_items = st.number_input("Number of Items", min_value=1, step=1)
for i in range(num_items):
    with st.expander(f"Item {i+1}"):
        name = st.text_input(f"Product {i+1}")
        hsn = st.text_input(f"HSN Code {i+1}")
        qty = st.number_input(f"Quantity {i+1}", min_value=1, step=1)
        rate = st.number_input(f"Rate {i+1}", min_value=0.0, step=0.01)
        items.append({"name": name, "hsn": hsn, "qty": qty, "rate": rate})

cgst_rate = st.number_input("CGST %", min_value=0.0, step=0.1, value=9.0)
sgst_rate = st.number_input("SGST %", min_value=0.0, step=0.1, value=9.0)

data = {
    "invoice_no": invoice_no,
    "invoice_date": invoice_date,
    "state": state,
    "state_code": state_code,
    "billed_to": billed_to,
    "billed_gstin": billed_gstin,
    "shipped_to": shipped_to,
    "shipped_gstin": shipped_gstin,
    "items": items,
    "cgst_rate": cgst_rate,
    "sgst_rate": sgst_rate
}

if st.button("Generate Invoice PDF"):
    pdf_path = generate_invoice(data)
    with open(pdf_path, "rb") as file:
        st.download_button("Download Invoice", file, file_name="invoice.pdf")
