import shutil
from pathlib import Path
import shutil
import numpy as np
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from PIL import Image as PILImage
import face_recognition 
import image_recognition as img_rec
from sqlalchemy import text

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# def is_face_duplicate(face_encodings, db):
#     if len(face_encodings) == 0:
#         raise ValueError("No faces detected in the uploaded image.")

#     distances = []

#     # Loop over each encoding in the database
#     for stored_face in db.query(models.UniqueFace).all():
#         stored_encoding = np.frombuffer(stored_face.encoding, dtype=np.float64)

#         # Compare with each stored encoding
#         for face_encoding in face_encodings:
#             # Make sure both encodings are NumPy arrays of the same shape
#             if stored_encoding.shape == face_encoding.shape:
#                 distance = np.linalg.norm(stored_encoding - face_encoding)
#                 distances.append(distance)
#             else:
#                 print(f"Shape mismatch: {stored_encoding.shape} vs {face_encoding.shape}")
# # Euclidean distance
#         for distances in distances:
#             if distances < 0.6:  # Threshold for considering it a match
#                 return True
    
#             return False
        
        # match = face_recognition.compare_faces([stored_encoding], face_encodings)
        
    #     if match[0]:  # If a match is found, return True (duplicate)
    #         return True
    # return False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload_group_photo")
async def upload_group_photo(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    
    contents = await file.read()

    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
    

    query = text("select * from images")
    result = db.execute(query)
    images = result.fetchall()
    if images:
        for image in images:
            print(image)
            if image[1] == file.filename:
                raise HTTPException(status_code=400, detail="Group photo already exists")

    db_image = models.Image(filename=file.filename, file_path=file_path)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

    recognized_people = img_rec.main(file_path)
    print(recognized_people)
    if not recognized_people:
        raise HTTPException(status_code=400, detail="No faces found in the group photo")
    else:
        query = text("select * from unique_faces")
        result = db.execute(query)
        
        data = result.fetchall()
        if data: 
            print("rrrrrrrrrrrrrr",data)
            for image in data:
                    for i in range(len(recognized_people)):
                        if recognized_people[i[0]] != image[1]:
                            db_unique_face = models.UniqueFace(
                                name = recognized_people[i][0],
                                image_id = db_image.id
                            )
                            db.add(db_unique_face)
                        
                        db.commit() 
                        db.refresh(db_unique_face)
                        name, image_path = recognized_people.pop(0)
                        db_face = models.Face(grp_id = db_image.id, unique_face_id = db_unique_face.unique_face_id)
                        db.add(db_face)
                        db.commit()
                        db.refresh(db_face)
        else:
            print("heloo..........")
            for i in recognized_people:
                db_unique_face = models.UniqueFace(
                    name = i[0],
                    image_id = db_image.id
                )
                db.add(db_unique_face)
                        
                db.commit() 
                db.refresh(db_unique_face)
                name, image_path = recognized_people.pop(0)
                db_face = models.Face(grp_id = db_image.id, unique_face_id = db_unique_face.unique_face_id)
                db.add(db_face)
                db.commit()
                db.refresh(db_face)
            db.commit()
            db.refresh(db_face)
                    
                

    
    return {"message": "Group photo uploaded and faces extracted successfully"}


@app.get("/faces_in_group/{image_id}")
def get_faces_in_group(image_id: int, db: Session = Depends(get_db)):
   
    faces = db.query(models.UniqueFace).filter(models.UniqueFace.image_id == image_id).all()
    return {"faces": [{"id": face.id, "name": face.name} for face in faces]}

