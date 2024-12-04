from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, LargeBinary, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from dataclasses import dataclass

CONNECT_STRING= "mysql+mysqlconnector://root:@localhost:3306/szakdolgozat"
engine = create_engine(CONNECT_STRING, echo=False)
Base = declarative_base()


@dataclass
class Customer(Base):
    __tablename__ = "customers"
    id : int = Column("id", Integer, Sequence("customers_id_seq"), primary_key=True)
    name : str = Column("name", String(length=255))
    postalCode : int = Column("postal_code", Integer)
    settlement : str = Column("settlement", String(length=255))
    address : str = Column("address", String(length=255))
    taxNumber : str = Column("tax_number", String(length=255))
    email : str = Column("email", String(length=255))
  

@dataclass
class Part(Base):
    __tablename__ = "parts"
    id: int = Column("id", Integer, Sequence("parts_id_seq"), primary_key=True)
    itemNumber: str = Column("item_number", String(length=255))
    name: str = Column("name", String(length=255))
    amount: int = Column("amount", Integer)
    price: int = Column("price", Integer)

@dataclass
class Bill(Base):
    __tablename__ = "bill"
    billId: int = Column("bill_id", Integer, primary_key=True)
    customerId: int = Column("customer_id", Integer)
    date: str = Column("date", String(length=255))
    itemList: str = Column("item_list", String(length=255))


@dataclass
class SoldPart(Base):
    __tablename__ = "sold_parts"
    spartId: int = Column("id", Integer, primary_key=True)
    partId: int = Column("part_id", Integer)
    customerId: int = Column("customer_id", Integer)
    amount: int = Column("amount", Integer)
    name: str = Column("name", String(length=255))
    price: int = Column("price", Integer)
    billId: int = Column("bill_id", Integer)
    sellDate: int = Column("sell_date", String(length=255))

def setup_database():
    Base.metadata.create_all(engine)


def get_customers():
    with Session(engine) as session:
        customer_dict = dict()
        customers = session.query(Customer).all()
        
        for customer in customers:
            customer_info = {
                'id' : customer.id,
                'name': customer.name,
                'postalCode': customer.postalCode,
                'settlement': customer.settlement,
                'address' : customer.address,
                'taxNumber' : customer.taxNumber,
                'email' : customer.email,
            }
            customer_dict[customer.id] = customer_info
        return customer_dict

        
def get_parts():
    with Session(engine) as session:
        parts_dict = dict()
        parts = session.query(Part).all()
        
        for part in parts:
            part_info = {
                'id' : part.id,
                'itemNumber' :  part.itemNumber,
                'name' : part.name,
                'netPrice' : part.netPrice,
                'discount': part.discount,
                'amount' : part.amount,
                'tax': part.tax,
                'price' : part.price,
            }
            parts_dict[part.id] = part_info
        return parts_dict
    
