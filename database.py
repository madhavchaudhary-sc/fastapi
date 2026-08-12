
# connection 


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker ,declarative_base


# username:password
db_url = "postgresql://postgres:admin123@localhost:5432/fastapi_db"

engine = create_engine(db_url)


SessionLocal = sessionmaker(autocommit =False ,
                            autoflush = False, 
                            bind=engine) 

#* bind=engine =Ye session kis database se connect hoga

#Base = declarative_base() bahut important hai. Isi ke through SQLAlchemy ko pata chalta hai ki kaun si Python classes database tables banengi.
Base = declarative_base()



