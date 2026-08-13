
# connection 


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker ,declarative_base


# username:password
# db_url = "postgresql://postgres:admin123@localhost:5432/fastapi_db"

#FASTAPI AND postgre ka alag containe rbanae ke baad local jost naam hata ke ,kyu ki Compose mein service ka naam:postgres:
db_url = "postgresql://postgres:admin123@postgres:5432/fastapi_db"

# FastAPI container
#       │
#       │ postgres:5432
#       ▼
# PostgreSQL container

engine = create_engine(db_url)


SessionLocal = sessionmaker(autocommit =False ,
                            autoflush = False, 
                            bind=engine) 

#* bind=engine =Ye session kis database se connect hoga

#Base = declarative_base() bahut important hai. Isi ke through SQLAlchemy ko pata chalta hai ki kaun si Python classes database tables banengi.
Base = declarative_base()



