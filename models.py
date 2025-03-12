# # from sqlalchemy import Column, Integer, String
# # from database import Base

# # class Image(Base):
# #     __tablename__ = "upload_images"

# #     id = Column(Integer, primary_key=True, index=True)
# #     filename = Column(String, nullable=False)
# #     file_path = Column(String, nullable=False) 


# # class Person(Base):
# #     __tablename__ = "person_images"
# #     id = Column(Integer, primary_key=True, index=True)
# #     filename = Column(String, nullable=False)
# #     file_path = Column(String, nullable=False) 
    
# from sqlalchemy import Column, Integer, String, LargeBinary
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine

# Base = declarative_base()

# class Image(Base):
#     __tablename__ = 'images'

#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String)
#     file_path = Column(String) 

# # Create a database connection
# SQLALCHEMY_DATABASE_URL = 'postgresql://shree:Tech%40123@localhost/Image_recognition'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

class UniqueFace(Base):
    __tablename__ = "unique_faces"

    unique_face_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True) 
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)  

class Face(Base):
    __tablename__ = "faces"
    id = Column(Integer, primary_key=True, index=True)
    grp_id = Column(Integer, ForeignKey("images.id"), nullable=False)  
    unique_face_id = Column(Integer, ForeignKey("unique_faces.unique_face_id"), nullable=False) 
    