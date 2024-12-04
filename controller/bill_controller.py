import os
from flask import Blueprint, jsonify, request, send_file
from model.models import Bill, Customer, Part, SoldPart, engine
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import fonts
from datetime import datetime
import io


bill = Blueprint('bill', __name__)


@bill.route('/createBill', methods=['GET','POST'])
def create_bill():
    if request.method == 'POST':
        with Session(engine) as session:
            bill_data = request.get_json()
            customer_id = int(bill_data['paramId'])
            customer_name = bill_data['paramName']
            customer_postalCode = bill_data['paramPostalCode']
            customer_settlement = bill_data['paramSettlement']
            customer_address = bill_data['paramAddress']
            customer_tax_number = bill_data['paramTaxNumber']
            sum_no_tax = bill_data['sum']
            sum_with_tax = bill_data['sumWithTax']
            billed_parts = bill_data['billedParts']

            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            fonts_directory = os.path.join(os.path.dirname(__file__), '../utils/fonts')
            dejavu_sans = os.path.join(fonts_directory, 'DejaVuSans.ttf')
            dejavu_sans_bold = os.path.join(fonts_directory, 'DejaVuSans-Bold.ttf')

            pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_sans))
            pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', dejavu_sans_bold))

            title = "Számla"
            bills = session.query(Bill).all()
            number_of_bills = len(bills)+1
            bill_number = f"KC-{number_of_bills:04d}" 
            
            p.setFont("DejaVuSans-Bold", 24)
            text_width = p.stringWidth(title, "DejaVuSans-Bold", 20)
            p.drawString((width - text_width) / 2, height - 50, title)

            p.setFont("DejaVuSans", 10)
            text_width = p.stringWidth(bill_number, "DejaVuSans", 10)
            p.setFillColorRGB(0.5, 0.5, 0.5)
            p.drawString((width - text_width) / 2, height - 65, bill_number)

            p.setStrokeColorRGB(0.7, 0.7, 0.7)
            p.setLineWidth(1) 
            p.line(50, height - 70, width-50, height - 70) 

            column_width = width / 2
            left_column_center = column_width / 2
            right_column_center = width - (column_width / 2)

            p.setFillColorRGB(0, 0, 0)
            p.setFont("DejaVuSans-Bold", 14)
            p.drawCentredString(left_column_center, height - 100, "Vevő")
            p.drawCentredString(right_column_center, height - 100, "Eladó")

            p.setFont("DejaVuSans", 12)
            p.drawString(70, height - 120, f"{customer_name}")
            p.drawString(70, height - 140, f"{customer_postalCode}, {customer_settlement}")
            p.drawString(70, height - 160, f"{customer_address}")
            p.drawString(70, height - 180, f"{customer_tax_number}")
            
            right_column_x = width - 70  # Right margin for the "Eladó" column
            p.drawRightString(right_column_x, height - 120, "KásaCar Kft.")
            p.drawRightString(right_column_x, height - 140, "6067, Tiszaalpár")
            p.drawRightString(right_column_x, height - 160, "Petőfi Sándor utca 72.")
            p.drawRightString(right_column_x, height - 180, "XXXXXX-X-XX")
            p.drawRightString(right_column_x, height - 200, "XXXXXXXX-XXXXXXXX")

            p.setFont("DejaVuSans-Bold", 16)
            parts_text = "Tételek"
            text_width = p.stringWidth(parts_text, "DejaVuSans", 16)
            p.drawString((width - text_width) / 2, height - 280, parts_text)

            x_item_number = 70
            x_name = 150  
            x_amount = 290
            x_price = 400 
            x_price_with_tax = 500

            y = height - 300

            p.setFont("DejaVuSans-Bold", 12)
            p.drawString(x_item_number, y, "Cikkszám")
            p.drawString(x_name, y, "Megnevezés")
            p.drawString(x_amount, y, "Mennyiség")
            p.drawString(x_price, y, "Nettó")
            p.drawString(x_price_with_tax, y, "Bruttó")


            p.setLineWidth(1)
            p.line(50, y - 10, width - 50, y - 10)

            y -= 20

            p.setFont("DejaVuSans", 10)
            for part in billed_parts:
                part_name = part['name']
                item_number = part['itemNumber']
                part_price = part['price']
                part_amount = part['amount']

                if len(part_name) > 25:
                    part_name = part_name[:25] + "..."

                p.drawString(x_item_number, y, str(item_number))
                p.drawString(x_name, y, part_name)
                p.drawString(x_amount+30, y, str(part_amount))
                p.drawString(x_price, y, f"{part_amount*part_price:.2f} Ft")
                p.drawString(x_price_with_tax, y, f"{part_amount*part_price*1.27:.2f} Ft")

                y -= 20

                p.line(50, y + 10, width - 50, y + 10)

            p.setFont("DejaVuSans", 16)
            p.drawString(70, y - 50, f"Nettó: {sum_no_tax} Ft")
            p.drawString(70, y - 70, f"Bruttó: {sum_with_tax} Ft")
            
            signature_y = y - 100
            p.setLineWidth(1)
            p.line(width - 170, signature_y, width - 70, signature_y)
            p.drawRightString(width - 70, signature_y - 15, "KásaCar Kft.") 

            p.setFillColorRGB(0.5, 0.5, 0.5)
            p.setFont("DejaVuSans", 10)
            creation_date = "Kiállítás dátuma:"
            text_width = p.stringWidth(creation_date, "DejaVuSans", 10)
            p.drawString((width - text_width) / 2, height - (height - 70), creation_date)

            
            today_date = datetime.today().strftime('%Y.%m.%d')
            text_width = p.stringWidth(today_date, "DejaVuSans", 10)
            p.drawString((width - text_width) / 2, height - (height - 50), today_date)

            
            p.showPage()
            p.save()
            buffer.seek(0)

            
            part_ids_list = [
                part['id'] for part in billed_parts if part['itemNumber'] != "Munka"
            ]
            part_ids_string = ','.join(map(str, part_ids_list))
            new_bill = Bill(billId=number_of_bills, date=today_date, customerId=customer_id, itemList=part_ids_string)
            
            session.add(new_bill)
            session.commit()

            for part in billed_parts:  
                sold_part_len = len(session.query(SoldPart).all())+1
                sold_part_insert = SoldPart(
                                    spartId=sold_part_len, 
                                    partId=part["id"], 
                                    customerId=customer_id, 
                                    amount=part["amount"],
                                    name=part["name"],
                                    price=part["price"],
                                    billId=number_of_bills,
                                    sellDate=today_date
                                )
                session.add(sold_part_insert)
                session.commit()
                
                part_in_db = session.query(Part).filter_by(id=part["id"]).first()
    
                if part_in_db:
                    new_amount = part_in_db.amount - part["amount"]
                    if new_amount <= 0:
                        session.delete(part_in_db)
                    else:
                        part_in_db.amount = new_amount
                        session.add(part_in_db)
                session.commit()

            return send_file(buffer, as_attachment=False, download_name=f'{bill_number}.pdf', mimetype='application/pdf')

        return jsonify({"error": "Invalid Method"}), 405
    
@bill.route('/getBillData', methods=['GET', 'POST'])
def get_bill_data():
    if request.method == 'GET':
        with Session(engine) as session:
            bills = session.query(Bill).all()
            bill_data = []

            for bill in bills:
                bill_id = bill.billId
                date = bill.date
                item_list = bill.itemList.split(',') if bill.itemList else []

                customer = session.query(Customer).filter_by(id=bill.customerId).first()
                customer_details = {
                    'customer_name': customer.name if customer else 'N/A',
                    'postal_code': customer.postalCode if customer else 'N/A',
                    'settlement': customer.settlement if customer else 'N/A',
                    'address': customer.address if customer else 'N/A',
                    'tax_number': customer.taxNumber if customer else 'N/A',
                }
        
                items = session.query(SoldPart).filter(SoldPart.partId.in_(item_list)).all()
                item_details = [
                    {
                        'item_id': item.partId,
                        'name': item.name,
                        'price': item.price,
                        'amount': item.amount,
                    }
                    for item in items
                ]

                bill_entry = {
                    'bill_id': bill_id,
                    'date': date,
                    'customer_details': customer_details,
                    'items': item_details,
                }

                bill_data.append(bill_entry)

            return jsonify(bill_data)

    return jsonify({"error": "Invalid Method"}), 405
