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
    pdf.set_font("Arial", "B", 10)  # Smaller font for GST and Mobile
    pdf.cell(50, 10, "GSTIN: 06APGPK2323H1Z8", align='L')

    pdf.set_font("Arial", "B", 20)  # Bigger font for PRITI ENTERPRISES
    pdf.cell(100, 10, "PRITI ENTERPRISES", align='C')

    pdf.set_font("Arial", "B", 10)  # Smaller font for GST and Mobile
    pdf.cell(50, 10, "Mobile: 9416083098, 9813269838", align='R', ln=True)

    pdf.set_font("Arial", "", 10)
    pdf.cell(200, 5, "Near Santu Tubwel, Tosham Road Baypass, Bhiwani - 127021 (Haryana)", ln=True, align='C')
    pdf.ln(5)

    
    # Invoice Details
    pdf.cell(100, 6, f"Invoice No: {data['invoice_no']}")
    pdf.cell(100, 6, f"Invoice Date: {data['invoice_date']}", ln=True)
    pdf.cell(100, 6, f"State: Haryana  State Code: 06")
    pdf.cell(100, 6, f"Reverse Charge: {data['reverse_charge']}", ln=True)
    pdf.cell(100, 6, f"E-Way Bill No: {data['eway_bill_no']}", ln=True)  # Added E-Way Bill No.
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

    # Tax Calculation (User input CGST, SGST, IGST)
    cgst = round(total * (data['cgst_rate'] / 100), 2)
    sgst = round(total * (data['sgst_rate'] / 100), 2)
    igst = round(total * (data['igst_rate'] / 100), 2)
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

    return pdf.output(dest='S').encode('latin1')

st.title("Invoice Generator")

# Invoice Details
invoice_no = st.text_input("Invoice No", "249")
invoice_date = st.date_input("Invoice Date", datetime.date.today()).strftime("%d-%m-%Y")
reverse_charge = st.selectbox("Reverse Charge", ["Y", "N"])

# **New Field: E-Way Bill Number**
eway_bill_no = st.text_input("E-Way Bill No", "")

# Billed To
billed_to_name = st.text_input("Billed To - Name")
billed_to_gstin = st.text_input("Billed To - GSTIN")
billed_to_address = st.text_area("Billed To - Address")
billed_to_state = st.text_input("Billed To - State")

# Shipped To
shipped_to_name = st.text_input("Shipped To - Name")
shipped_to_gstin = st.text_input("Shipped To - GSTIN")
shipped_to_address = st.text_area("Shipped To - Address")
shipped_to_state = st.text_input("Shipped To - State")

# Tax Rates (User Input)
cgst_rate = st.number_input("CGST Rate (%)", min_value=0.0, step=0.1, format="%.1f")
sgst_rate = st.number_input("SGST Rate (%)", min_value=0.0, step=0.1, format="%.1f")
igst_rate = st.number_input("IGST Rate (%)", min_value=0.0, step=0.1, format="%.1f")

# Generate Invoice Button
if st.button("Generate Invoice"):
    invoice_data = locals()
    pdf = generate_invoice(invoice_data)
    st.download_button("Download Invoice", pdf, "invoice.pdf", "application/pdf")
