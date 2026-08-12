
#! basic starting
# from fastapi import FastAPI

# app =FastAPI()

# def greet():
#     return "welcome to apna college"


# o/p = {"detail":"Not Found"}

#! start normal class and const bana ke data dekha on website

# from model import Product
# from fastapi import FastAPI            # FastAPI class import kar rahe hain.

# app =FastAPI()           #Ye hamara application object hai.


# @app.get("/")               # ab app fastapi hai or uss me bahut method hai
# def greet():
#  return "welcome to apna college"


# Product =[
#    Product(1,"phone","buget phone",99,2),
#    Product(2,"iphone","buget phone",49,7)
   
# ]


# @app.get("/products")
# def get_all_product():
#     return Product





#! ab pydantic bana ke dekhege jo const banane ki jarurat nhi hoti
#? swagger bhi dene mila idhar /docs likho bas

from model import Product
from fastapi import FastAPI , HTTPException ,Depends  
from database import engine, SessionLocal 
import database_model 
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware      

app =FastAPI()     


# --------cors by default it is block so fastpi port orgin se permission denge hum 
# humne isse concept_main wale me samjhaya hai
# permission dena

app.add_middleware(
    CORSMiddleware,             
    allow_origins =["http://localhost:3000"], #origins s last me imp hai left hua to err #Multiple origins bhi de sakte ho , allow_origins=[ "http://localhost:3000","http://localhost:5173",]
    allow_methods=["*"],     #Saare HTTP methods allow: GET, POST, PUT, DELETE, etc.
    allow_credentials=True ,  #Cookies, Authorization headers, sessions use kar sakte ho
    allow_headers=["*"]   #Saare request headers allow.
)



# this will create table product in db (base database_model me inher ka kam kiya ab meta data class ka use krne me help karega)
database_model.Base.metadata.create_all(bind=engine)

@app.get("/")               
def greet():
 return "welcome to apna college"


# name convetion shi rakhna list me p small andhar obj ka P cap or class P cap me rakhna (pydantic me aise he likhna padhta hai id= 1,name= "phone") tahi pydantic smjhata hai
products =[
   Product(
        id=1,
        name="phone",
        description="budget phone",
        price=99,
        quantity=2
    ),
    Product(
        id=2,
        name="iphone",
        description="budget phone",
        price=49,
        quantity=7
    )
   
]

# bar bar db =SessionLocal() krna padhe connection open close krne ke liye isliye ek separte function he bana diya
def get_db():
   db =SessionLocal()
   try:
      yield db
   finally:
      db.close()  
   
#? (concept_of_main file me under karu isse)
# upar banaye products ko db me dalan iss ke through
def init_db():
   db = SessionLocal()

    #fetch --> query & add --> post data in db
    # u can have multiple model & here we specific table & this line give count in table
   count =db.query(database_model.Product).count()

   if count ==0:
      for product in products:
         #db.add(product)  --> you cannot pass hai obj of product bcz it is link with pydantic Product obj so we have to pass obj of sqlalchemy database_model.Product
         db.add(database_model.Product(**product.model_dump())) #.Product have feature it will ccept key value pair and make obj  # how product will convert into obj of sqqlalchemy database_model.Product(product) this will give key value pair 
          #product is objline no -61 &77 and .model_dump() -> into dictionary(acourse this will have key value but) & -> dic ko key value pair banane ke liye unpackage krege ** laga ke key value pair mile
   db.commit() 

init_db()         

#? ache se logic likh ke niche banaya 
# @app.get("/products/{id}")              # dynamic banaya {}
# def get_all_product(id:int):            # pass kiya 
#     return product[id-1]            #id-1 = index dega element ka # p small rakhna list wala idhar hai

# ---------------------------------------
#? before db

# @app.get("/products")
# def get_all_product():
#     return products



#?after db
@app.get("/products")              
def get_all_product(db:Session= Depends(get_db)):    # db=session() ki jagah db: Session =depend(get_db) likha in ()
    
    db_products = db.query(database_model.Product).all()
    

    return db_products
# ------------------------------------

#?before db
# @app.get("/products/{id}")
# def get_idwise_product(id: int):
#     for product in products:
#         if product.id == id:
#             return product

#     raise HTTPException(status_code=404, detail="Product not found")

#?after db 
@app.get("/products/{id}")              
def get_idwise_product(id:int,db:Session= Depends(get_db)): 
    db_product =db.query(database_model.Product).filter(database_model.Product.id ==id).first()
    if db_product:  
           return db_product


    #return "product not found"   #* Real APIs me string return karne ki jagah proper HTTP error dete hain.
    raise HTTPException(status_code=404, detail="Product not found")      # json me data aayega




# -----------------------------------------------
#?before db
# @app.post("/product")
# def add_product(product:Product):
#    products.append(product)
#    return products


#?after db (concept_of_main file me under karu isse)
# @app.post("/products")
# def add_product(product:Product,db:Session= Depends(get_db)):
#    db_product =db.add(database_model.Product(**product.model_dump()))
#    db.commit()                        #Database me permanently save kar diya.
#    db.refresh(db_product)             #Database se latest data wapas object me le aaya.Ye especially tab useful hota hai jab id auto-generate hoti hai.
                                # ye kuch nhi karta none dega o/p #db.add session me add karta hai


#chatgpt app.post 
@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):

    db_product = database_model.Product(**product.model_dump())

    db.add(db_product)  # ye none return karta hai

    db.commit()

    db.refresh(db_product)

    return db_product

# diff samjho 
# ❌ Ye galat hai:

# db_product = db.add(...)

# Kyunki:

# print(db.add(...))

# Output:

# None

# --------------------------------------------


#?before db
# @app.put("/product")
# def update_product(id:int,product:Product):
#     for i in range(len(products)):
#       if products[i].id == id:
#          products[i] = product
#          return "Product added successfull"
      
#     return " no product found"  


#? after (concept_of_main file me under karu isse)
@app.put("/products/{id}")
def update_product(id:int,product:Product,db:Session =Depends(get_db)):
    # first we have to check product exist or not db.query will give product
    db_product =db.query(database_model.Product).filter(database_model.Product.id ==id).first()
    if db_product:                  # if db_product exist iska matlab hai
       db_product.name = product.name
       db_product.description = product.description
       db_product.price = product.price
       db_product.quantity = product.quantity
       db.commit()
       db.refresh(db_product)
       return "product updated"
      #  return db_product
     
       
    else:
       return "no product found"
    
    








    

# -----------------------------------


#?before db
# @app.delete("/product")
# def delete_product(id:int):
#    for i in range(len(products)):
#        if products[i].id == id:
#          del products[i]
#          return "product deleted"
       
#    return "product  deleted"   

#?after db

@app.delete("/products/{id}")
def delete_product(id:int,db:Session =Depends(get_db)):
   # first we have to fetch data from db
       db_product =db.query(database_model.Product).filter(database_model.Product.id ==id).first()
       if db_product:
           db.delete(db_product)
           db.commit()
           return "deleted your option"
       else:
               return "no product found"
        
# product: Product    ye hatane bol raha hai kyu ki fastapi react req se body bhi mang raha hai
# Is request me body nahi hoti, lekin tum FastAPI ko bol rahe ho ki product: Product bhi chahiye.

# Isliye FastAPI bol raha hai:

# 422 Unprocessable Content (required request body missing)        

#? Ye yaad rakhna
# API	Body chahiye?
# GET	❌ Nahi
# DELETE	❌ Nahi
# POST	✅ Haan
# PUT	✅ Haan