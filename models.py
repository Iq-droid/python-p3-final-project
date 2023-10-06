from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Vehicle(Base):
    __tablename__ = 'vehicles'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    brand = Column(String)
    condition = Column(String)
    
    #1 to 1 rel with rev tbl
    reviews = relationship('Review', back_populates='vehicle')
    
class Buyer(Base):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    contact = Column(String)
    
    #1 to many rel with rev tbl
    reviews = relationship('Review', back_populates='buyer')
    
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    rating = Column(Integer)
    comment = Column(String)
    
    #many to 1 rel with veh and byr tbl
    vehicle_id = relationship('Vehicle', back_populates='reviews')
    buyer = relationship('Buyer', back_populates='reviews')
    
class SoldVehicle(Base):
    __tablename__ = 'sold_vehicles'
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'))
    buyer_id = Column(Integer, ForeignKey('buyers.id'))
    
    #many to 1 rel with veh and byr tbl
    vehicle = relationship('Vehicle')
    buyer = relationship('Buyer')
    
    #defining func for db operations
def create_tables(engine):
    Base.metadata.create_all(engine)
    
def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()

def add_review(session, vehicle_type, brand, condition, buyer_name, contact, rating, comment):
     new_vehicle = Vehicle(type=vehicle_type, brand=brand, condition=condition)
     new_buyer = Buyer(name=buyer_name, contact=contact)
     session.add_all([new_vehicle, new_buyer])
     session.commit()
     new_review = Review(vehicle_id=new_vehicle.id, buyer_id=new_buyer.id, rating=rating, comment=comment)
     session.add(new_review)
     session.commit()
     return new_review