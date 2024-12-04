from flask import Blueprint, jsonify, request
from model.models import Customer, engine
from sqlalchemy.orm import Session
from sqlalchemy import desc

customers = Blueprint("customers", __name__)


@customers.route('/getCustomers', methods=['GET'])
def get_customers():
     if request.method == 'GET':
          customer_dict = dict()
          with Session(engine) as session:
               customers = session.query(Customer).order_by(Customer.name).all()
               max_index_query = session.query(Customer.id).order_by(desc(Customer.id)).first()
          
               i = 0
               for customer in customers:
                    customer_info = {
                         'id' : customer.id,
                         'name' : customer.name,
                         'postalCode' : customer.postalCode,
                         'settlement' : customer.settlement,
                         'address' : customer.address,
                         'taxNumber' : customer.taxNumber,
                         'email' : customer.email,
                    }
                    customer_dict[i] = customer_info
                    i += 1
          if max_index_query:
               max_index = max_index_query[0]
               max_index = int(max_index)+1

          resp_object = {'status': 'success', 'message' : 'Query completed'}
          resp_object['customers'] = customer_dict
          resp_object['nextCustomerIndex'] = max_index
          return jsonify(resp_object)
          

@customers.route('/addCustomer', methods=['GET', 'POST'])
def add_customer():
     if request.method == 'POST':
          post_data = request.get_json()
          customer_to_add = Customer(**post_data)
          with Session(engine) as session:
               session.add(customer_to_add)
               session.commit()
     return jsonify({'status' : 'success', 'message': 'Successfully added customer'})


@customers.route('/updateCustomer', methods=['GET', 'POST'])
def update_customer():
     with Session(engine) as session:
          if request.method == 'POST':
               post_data = request.get_json()
               customer_to_update = Customer(**post_data)
               with Session(engine) as session:
                    session.query(Customer).filter(Customer.id == customer_to_update.id).update({
                          Customer.address : customer_to_update.address,
                          Customer.settlement : customer_to_update.settlement,
                          Customer.email : customer_to_update.email,
                          Customer.taxNumber : customer_to_update.taxNumber,
                          Customer.postalCode : customer_to_update.postalCode
                         }
                    )
                    session.commit()
          return jsonify({'status' : 'success', 'message' : 'Update successful'})
     
     
@customers.route('/deleteCustomer', methods=['GET', 'POST'])
def delete_customer():
     if request.method == 'POST':
          post_data = request.get_json()
          with Session(engine) as session:
               session.query(Customer).filter(Customer.id==(int)(post_data)).delete()
               session.commit()
     return jsonify({'status' : 'success', 'message': 'Deletion successful'})