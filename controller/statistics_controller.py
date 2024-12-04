from flask import Blueprint, jsonify, request
from model.models import SoldPart, Customer, engine
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta


statistics = Blueprint('statistics', __name__)

@statistics.route('/getStatistics', methods=['GET', 'POST'])
def get_stats():
    if request.method == 'GET':
        monthly_sales = dict()
        annual_sales = 0
        highest_customer_name = ""
        highest_customer_sales = 0
        most_bills_customer_name = ""
        most_bills_count = 0

        with Session(engine) as session:
            today = datetime.today()
            twelve_months_ago = today - timedelta(days=365)
            current_month_year = today.strftime('%Y.%m')
            twelve_months_ago_str = twelve_months_ago.strftime('%Y.%m')

        
            sales_data = session.query(
                func.substring(SoldPart.sellDate, 1, 7).label('month_year'), 
                func.sum(SoldPart.price * SoldPart.amount).label('total_sales') 
            ).filter(
                func.substring(SoldPart.sellDate, 1, 7) >= twelve_months_ago_str  
            ).group_by('month_year').order_by('month_year').all()

            for record in sales_data:
                month_year = record[0] 
                total_sales = record[1]  
                monthly_sales[month_year] = total_sales
                annual_sales += total_sales 

            highest_customer_query = session.query(
                SoldPart.customerId,
                func.sum(SoldPart.price * SoldPart.amount * 1.27).label('total_customer_sales')
            ).group_by(SoldPart.customerId).order_by(func.sum(SoldPart.price * SoldPart.amount * 1.27).desc()).first()

            if highest_customer_query:
                highest_customer_id = highest_customer_query[0]
                highest_customer_sales = highest_customer_query[1]

                customer = session.query(Customer).filter_by(id=highest_customer_id).first()
                highest_customer_name = customer.name if customer else "Unknown"

            most_bills_customer_query = session.query(
                SoldPart.customerId,
                func.count(func.distinct(SoldPart.billId)).label('bill_count')
            ).group_by(SoldPart.customerId).order_by(func.count(func.distinct(SoldPart.billId)).desc()).first()

            if most_bills_customer_query:
                most_bills_customer_id = most_bills_customer_query[0]
                most_bills_count = most_bills_customer_query[1]

                customer = session.query(Customer).filter_by(id=most_bills_customer_id).first()
                most_bills_customer_name = customer.name if customer else "Unknown"

            return jsonify({
                'monthly_sales': monthly_sales,
                'annual_sales': annual_sales,
                'highest_customer': {
                    'name': highest_customer_name,
                    'total_sales': highest_customer_sales
                },
                'most_bills_customer': {
                    'name': most_bills_customer_name,
                    'bill_count': most_bills_count
                }
            })

    return "Invalid method", 405
