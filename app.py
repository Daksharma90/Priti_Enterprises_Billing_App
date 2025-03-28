import streamlit as st
from fpdf import FPDF
import datetime
from num2words import num2words  


def generate_invoice(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)

    # 1. Invoice Header (Company Information)
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "PRITI ENTERPRISES", align='C', ln=True)  # Prominent Company Name
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 5, "Near Santu Tubwel, Tosham Road Baypass, Bhiwani - 127021 (Haryana)", align='C', ln=True)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 5, f"GSTIN: 06APGPK2323H1Z8", ln=False)
    pdf.cell(0, 5, f"Mobile: 9416083098, 9813269838", ln=True, align='R')
    pdf.ln(5)

    # 2. Recipient Details (Billed To / Shipped To)
    pdf.set_fill_color(240, 240, 240)  # Light gray background
    pdf.set_line_width(0.1)
    pdf.rect(10, pdf.y, 90, 40, 'DF')  # Box around Billed To
    pdf.rect(110, pdf.y, 90, 40, 'DF')  # Box around Shipped To
    pdf.set_font("Arial", "B", 10)
    pdf.text(12, pdf.y + 5, "Billed To:")
    pdf.text(112, pdf.y + 5, "Shipped To:")
    pdf.set_font("Arial", "", 10)
    pdf.text(12, pdf.y + 12, f"Name: {data['billed_to_name']}")
    pdf.text(112, pdf.y + 12, f"Name: {data['shipped_to_name']}")
    pdf.text(12, pdf.y + 20, f"Address: {data['billed_to_address']}")
    pdf.text(112, pdf.y + 20, f"Address: {data['shipped_to_address']}")
    pdf.text(12, pdf.y + 28, f"GSTIN: {data['billed_to_gstin']}")
    pdf.text(112, pdf.y + 28, f"GSTIN: {data['shipped_to_gstin']}")
    pdf.text(12, pdf.y + 36, f"State: {data['billed_to_state']}")
    pdf.text(112, pdf.y + 36, f"State: {data['shipped_to_state']}")
    pdf.ln(45)

    # 3. Invoice Details (Invoice No, Date, etc.)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 6, "Invoice No:", border=1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(50, 6, data['invoice_no'], border=1)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 6, "Invoice Date:", border=1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, data['invoice_date'], border=1, ln=True)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 6, "Reverse Charge:", border=1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(50, 6, data['reverse_charge'], border=1)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 6, "State & Code:", border=1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, "Haryana 06", border=1, ln=True)
    pdf.ln(5)

    # 4. Product/Service Details (Table)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(10, 8, "Sr.", border=1, align='C')
    pdf.cell(80, 8, "Product / Service", border=1, align='C')
    pdf.cell(20, 8, "HSN/SAC", border=1, align='C')
    pdf.cell(15, 8, "Qty", border=1, align='C')
    pdf.cell(20, 8, "Rate", border=1, align='C')
    pdf.cell(30, 8, "Amount", border=1, align='C', ln=True)

    pdf.set_font("Arial", "", 10)
    total = 0
    for i, product in enumerate(data['products']):
        amount = round(product['qty'] * product['rate'], 2)
        total += amount
        pdf.cell(10, 6, str(i + 1), border=1, align='C')
        pdf.cell(80, 6, product['name'], border=1)
        pdf.cell(20, 6, product['hsn_sac'], border=1, align='C')
        pdf.cell(15, 6, str(product['qty']), border=1, align='C')
        pdf.cell(20, 6, f"{product['rate']:.2f}", border=1, align='R')
        pdf.cell(30, 6, f"{amount:.2f}", border=1, align='R', ln=True)
    pdf.ln(5)

    # 5. Tax Calculation
    pdf.cell(145, 6, "Total Amount Before Tax:", border=0, align='R')
    pdf.cell(30, 6, f"{total:.2f}", border=1, ln=True)

    cgst = round(total * (data['cgst_rate'] / 100), 2)
    sgst = round(total * (data['sgst_rate'] / 100), 2)
    igst = round(total * (data['igst_rate'] / 100), 2)
    total_after_tax = round(total + cgst + sgst + igst, 2)

    # Display CGST, SGST, and IGST even if zero
    pdf.cell(145, 6, f"CGST ({data['cgst_rate']}%)", border=0, align='R')
    pdf.cell(30, 6, f"{cgst:.2f}", border=1, ln=True)

    pdf.cell(145, 6, f"SGST ({data['sgst_rate']}%)", border=0, align='R')
    pdf.cell(30, 6, f"{sgst:.2f}", border=1, ln=True)

    pdf.cell(145, 6, f"IGST ({data['igst_rate']}%)", border=0, align='R')
    pdf.cell(30, 6, f"{igst:.2f}", border=1, ln=True)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(145, 6, "Total Amount After Tax:", border=0, align='R')
    pdf.cell(30, 6, f"{total_after_tax:.2f}", border=1, ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.ln(5)

    # 6. Amount in Words
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "Amount in Words:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, num2words(total_after_tax, lang='en').capitalize() + " only", ln=True)
    pdf.ln(5)

    # 7. Transportation Details (Tabular Format)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "Transportation Details", ln=True)

    # Table Headers
    pdf.cell(40, 6, "Transportation Mode", border=1)
    pdf.cell(40, 6, "Vehicle Number", border=1)
    pdf.cell(40, 6, "Date of Supply", border=1)
    pdf.cell(40, 6, "Place of Supply", border=1)
    pdf.cell(40, 6, "E-Way Bill No", border=1, ln=True)

    # Table Data
    pdf.set_font("Arial", "", 10)
    pdf.cell(40, 6, data['transportation_mode'], border=1)
    pdf.cell(40, 6, data['vehicle_number'], border=1)
    pdf.cell(40, 6, data['date_of_supply'], border=1)
    pdf.cell(40, 6, data['place_of_supply'], border=1)
    pdf.cell(40, 6, data['eway_bill_number'], border=1, ln=True)
    pdf.ln(5)

    # 8. Footer (Bank Details, Terms & Conditions)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "Bank Details:", ln=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, "Bank Name: Punjab National Bank", ln=True)
    pdf.cell(0, 6, "Account No.: 005308700006153", ln=True)
    pdf.cell(0, 6, "IFSC Code: PUNB0005300", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "Terms & Conditions:", ln=True)
    pdf.set_font("Arial", "", 8)
    pdf.cell(0, 5, "1. Goods once sold will not be taken back.", ln=True)
    pdf.cell(0, 5, "2. Interest @18% p.a. will be charged if payment is not made in stipulated time.", ln=True)
    pdf.cell(0, 5, "3. Subject to BHIWANI Jurisdiction Only.", ln=True)
    pdf.ln(5)

    pdf.cell(0, 5, "For: PRITI ENTERPRISES", ln=True, align='R')
    pdf.cell(0, 5, "Authorized Signatory", align='R')

    return pdf.output(dest='S').encode('latin1')


# Streamlit UI (Remains largely the same)
st.title("Invoice Generator")

# Invoice Details
invoice_no = st.text_input("Invoice No", "249")
invoice_date = st.date_input("Invoice Date", datetime.date.today()).strftime("%d-%m-%Y")
reverse_charge = st.selectbox("Reverse Charge", ["Y", "N"])

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

# Transportation Details
transportation_mode = st.text_input("Transportation Mode")
vehicle_number = st.text_input("Vehicle Number")
date_of_supply = st.date_input("Date of Supply", datetime.date.today()).strftime("%d-%m-%Y")
place_of_supply = st.text_input("Place of Supply")
eway_bill_number = st.text_input("E-Way Bill Number")  # Input for E-Way Bill Number

# Tax Rates (User Input)
cgst_rate = st.number_input("CGST Rate (%)", min_value=0.0, step=0.1, format="%.1f")
sgst_rate = st.number_input("SGST Rate (%)", min_value=0.0, step=0.1, format="%.1f")
igst_rate = st.number_input("IGST Rate (%)", min_value=0.0, step=0.1, format="%.1f")

# Product Details
st.subheader("Products / Services")
products = []
n = st.number_input("Number of Products", min_value=1, step=1)
for i in range(n):
    st.write(f"### Product {i+1}")
    name = st.text_input(f"Product {i+1} Name", key=f"name_{i}")
    hsn_sac = st.text_input(f"Product {i+1} HSN/SAC Code", key=f"hsn_{i}")
    qty = st.number_input(f"Product {i+1} Quantity", min_value=1, key=f"qty_{i}")
    rate = st.number_input(f"Product {i+1} Rate", min_value=0.0, format="%.2f", key=f"rate_{i}")
    products.append({"name": name, "hsn_sac": hsn_sac, "qty": qty, "rate": rate})

if st.button("Generate Invoice"):
    invoice_data = locals()
    pdf = generate_invoice(invoice_data)
    st.download_button("Download Invoice", pdf, "invoice.pdf", "application/pdf")
