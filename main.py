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

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def is_face_duplicate(face_encodings, db):
    if len(face_encodings) == 0:
        raise ValueError("No faces detected in the uploaded image.")

    distances = []

    # Loop over each encoding in the database
    for stored_face in db.query(models.UniqueFace).all():
        stored_encoding = np.frombuffer(stored_face.encoding, dtype=np.float64)

        # Compare with each stored encoding
        for face_encoding in face_encodings:
            # Make sure both encodings are NumPy arrays of the same shape
            if stored_encoding.shape == face_encoding.shape:
                distance = np.linalg.norm(stored_encoding - face_encoding)
                distances.append(distance)
            else:
                print(f"Shape mismatch: {stored_encoding.shape} vs {face_encoding.shape}")
# Euclidean distance
        for distances in distances:
            if distances < 0.6:  # Threshold for considering it a match
                return True
    
            return False
        
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
        # shutil.copyfileobj(contents, f)
    
    
    image = PILImage.open(file_path)
    image_np = np.array(image)
    print(image_np)
    
    # Detect face locations and extract their encodings using face_recognition
    face_locations = face_recognition.face_locations(image_np)
    face_encodings = face_recognition.face_encodings(image_np, face_locations)

    
    if face_encodings is None:
        raise HTTPException(status_code=400, detail="No face detected in the image")

    if is_face_duplicate(face_encodings, db):
        return {"message": "This face is already in the database. Duplicate not inserted."}
    
    db_image = models.Image(filename=file.filename, file_path=file_path)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)

   
    for encoding in face_encodings:
        encoding_bytes = encoding.tobytes()  
       
        db_face = models.UniqueFace(
            encoding=encoding_bytes,
            image_id=db_image.id,  
        )
        db.add(db_face)

    db.commit() 
    return {"message": "Group photo uploaded and faces extracted successfully"}

@app.get("/faces_in_group/{image_id}")
def get_faces_in_group(image_id: int, db: Session = Depends(get_db)):
   
    faces = db.query(models.UniqueFace).filter(models.UniqueFace.image_id == image_id).all()
    return {"faces": [{"id": face.id, "name": face.name,"encodig": face.encoding} for face in faces]}

