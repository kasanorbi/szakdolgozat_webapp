from flask import Blueprint, jsonify, request
from model.models import Part, engine
from sqlalchemy.orm import Session
from sqlalchemy import desc


components = Blueprint('components', __name__)


@components.route('/getComponents', methods=['GET'])
def get_parts():
     if request.method == 'GET':
          parts_dict = dict()
          with Session(engine) as session:
               parts = session.query(Part).all()
               max_index_query = session.query(Part.id).order_by(desc(Part.id)).first()

               i = 0
               for part in parts:
                    part_info = {
                         'id' : part.id,
                         'itemNumber' : part.itemNumber,
                         'name' : part.name,
                         'amount' : part.amount,
                         'price' : part.price
                    }
                    parts_dict[i] = part_info
                    i += 1

          if max_index_query:
               max_index = max_index_query[0]
               max_index = int(max_index)+1 
          resp_object = {'status': 'success', 'message' : 'Query completed'}
          resp_object['parts'] = parts_dict
          resp_object['nextPartIndex'] = max_index
          return jsonify(resp_object)


@components.route('/getComponentById/<int:part_id>', methods=['GET'])
def get_part_by_id(part_id):
     if request.method == 'GET':
          print(part_id)
          with Session(engine) as session:
               part = session.query(Part).filter_by(id=part_id).first()
               if part:
                    part_info = {
                         'id' : part.id,
                         'itemNumber' : part.itemNumber,
                         'name' : part.name,
                         'amount' : part.amount,
                         'price' : part.price
                    }
                    resp_object = {'status' : 'success', 'message': 'Query completed'}
                    resp_object['part'] = part_info
                    return jsonify(resp_object)
               else:
                    return jsonify({'status': 'error', 'message': 'Part not found'})


@components.route('/addComponent', methods=['GET', 'POST'])
def add_part():
     if request.method == 'POST':
          post_data = request.get_json()
          part_to_add = Part(**post_data)
          with Session(engine) as session:
               session.add(part_to_add)
               session.commit()
     return jsonify({'status' : 'success', 'message': 'Successfully added component'})


@components.route('/updateComponent', methods=['GET', 'POST'])
def update_part():
     with Session(engine) as session:
          if request.method == 'POST':
               post_data = request.get_json()
               component_to_update = Part(**post_data)
               with Session(engine) as session:
                    session.query(Part).filter(Part.id == component_to_update.id).update(
                         {
                          Part.itemNumber : component_to_update.itemNumber,
                          Part.name : component_to_update.name,
                          Part.amount : component_to_update.amount,
                          Part.price : component_to_update.price
                         }
                    )
                    session.commit()
          return jsonify({'status' : 'success', 'message' : 'Update successful'})


@components.route('/deleteComponent', methods=['GET', 'POST'])
def delete_part():
     if request.method == 'POST':
          post_data = request.get_json()
          print(post_data)
          with Session(engine) as session:
               session.query(Part).filter(Part.id==(int)(post_data)).delete()
               session.commit()
     return jsonify({'status' : 'success', 'message': 'Deletion successful'})
