from flask import Blueprint, jsonify, request
from model.models import Part, engine
from sqlalchemy.orm import Session
from sqlalchemy import desc
from scan.scan_utility import scan as scan_image
from scan.ocr import image_to_dict
import pythoncom

scan = Blueprint('scan', __name__)

@scan.route('/scan', methods=['GET'])
def start_scan():
    try:
        pythoncom.CoInitialize()
        scan_image()
        ocr()
    except Exception as e:
        return jsonify({'error': str(e)}), 501
    
@scan.route('/ocr', methods=['GET'])
def ocr():
    products_dict = image_to_dict("temp.jpeg")
    seperate_products = []
    
    with Session(engine) as session:
        max_index_query = session.query(Part.id).order_by(desc(Part.id)).first()
        if max_index_query:
               max_index = max_index_query[0]
               start_index = int(max_index)+1 
        
        for i in range(len(products_dict['itemNumber'])):
            part_instance = Part(
                id = start_index + i,
                itemNumber=products_dict['itemNumber'][i],
                name=products_dict['name'][i],
                amount=int(products_dict['amount'][i]),
                price=int(products_dict['price'][i])
            )
            if part_instance.amount == 0:
                 part_instance.amount += 1
            seperate_products.append(part_instance)
    
    with Session(engine) as session:
         for i in range(len(seperate_products)):
              session.add(seperate_products[i])
              session.commit()   
    return jsonify({'status' : 'success', 'message': 'Successfully added component'})
    