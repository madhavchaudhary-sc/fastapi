
from sqlalchemy import Column,Integer ,String,Float
# from sqlalchemy.ext.declarative import declarative_base
# Base =declarative_base()     # this function will create base for you for inhert
from database import Base

class Product(Base):       # base will make let know Db is link to Product table

    __tablename__ = "product"

    id= Column(Integer,primary_key =True,index =True)#autoincrement=True , ndustry me normally user se ID nahi li jaati. Database khud generate karta hai.Aur React form se ID field hata dete hain.
    name=Column(String)
    description= Column(String)
    price= Column(Float)
    quantity = Column(Integer)



#! Ye correct relationship hai.
# database.py
#      │
#      └── Base
#           │
#           ▼
# database_model.py
#           │
#           └── Product