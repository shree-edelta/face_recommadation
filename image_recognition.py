import face_recognition
import numpy as np
from PIL import Image
import os
import cv2
import uuid
import hashlib

def generate_random_id():
    return str(uuid.uuid4())

# Step 1: Load known faces (encode the known people).
def load_known_faces():
    known_faces = []
    known_names = []

    person_image = face_recognition.load_image_file("/Users/bhavik/Desktop/face_recognition_fastapi/uploads/srk.jpeg")  
    person_encoding = face_recognition.face_encodings(person_image)[0]
    known_faces.append(person_encoding)
    def generate_image_id(image):
    # Read image content as bytes
        image_bytes = image.file.read()
        
        # Create a hash of the image content (SHA-256 is a good choice)
        image_hash = hashlib.sha256(image_bytes).hexdigest()
        
        # Generate a UUID based on the image hash to ensure uniqueness
        image_id = uuid.uuid5(uuid.NAMESPACE_DNS, image_hash)
        
        return str(image_id)
    known_names.append(generate_image_id(person_image()) ) 
    print(known_faces, known_names)
    return known_faces, known_names



def get_face_encodings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    return face_encodings

def recognize_faces_in_group(image_encodings, known_faces, known_names):
    recognized_people = []

    for face_encoding in image_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.6)

        if True in matches:
            first_match_index = matches.index(True)
            recognized_people.append(known_names[first_match_index])  

    return recognized_people

def recognize_faces_in_group_photo(group_photo_path):
    
    known_faces, known_names = load_known_faces()

    image_encodings = get_face_encodings(group_photo_path)

    if len(image_encodings) == 0:
        print("No faces found in the image.")
        return []

    
    recognized_people = recognize_faces_in_group(image_encodings, known_faces, known_names)

    if not recognized_people:
        print("No recognized faces found in the image.")
        return []

    return recognized_people


# Main execution
if __name__ == "__main__":
    group_photo_path = "/Users/bhavik/Desktop/face_recognition_fastapi/uploads/psd.jpeg"

 
    
    image = cv2.imread(group_photo_path)

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_image)


    for top, right, bottom, left in face_locations:
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)


    cv2.imshow("Group Image with Faces", image)

    # Wait for any key press to close the image window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    recognized_people = recognize_faces_in_group_photo(group_photo_path)
    if recognized_people:
        print(f"Recognized people: {', '.join(recognized_people)}")
    else:
        print("No recognized faces.")


# import hashlib
# import uuid
# import numpy as np
# import cv2  # Using OpenCV for image processing

# # Function to generate a unique ID based on image content (using SHA-256 hash)
# def generate_image_id(image: np.ndarray):
#     # Convert image to bytes
#     _, buffer = cv2.imencode('.jpg', image)  # Convert the image to a byte format (JPEG in this case)
#     image_bytes = buffer.tobytes()  # Convert the buffer into bytes
    
#     # Create a hash of the image content (SHA-256)
#     image_hash = hashlib.sha256(image_bytes).hexdigest()
    
#     # Generate a UUID based on the image hash to ensure uniqueness
#     image_id = uuid.uuid5(uuid.NAMESPACE_DNS, image_hash)
    
#     return str(image_id)

# # Simulate reading the image for recognition (use OpenCV to load the image)
# def person_image(image_path: str) -> np.ndarray:
#     # Load the image using OpenCV (this will return a numpy array)
#     image = cv2.imread(image_path)
#     return image

# # Loading known faces (example)
# def load_known_faces():
#     known_faces = []
#     known_names = []

#     # Example: Load an image and generate its ID
#     image_path = "path_to_some_image.jpg"
#     image = person_image(image_path)  # Read image as numpy array
    
#     # Generate a unique ID for the image
#     image_id = generate_image_id(image)
    
#     # Append to known names
#     known_names.append(image_id)
    
#     return known_faces, known_names

# # Example of using the above function to generate image IDs
# known_faces, known_names = load_known_faces()
# print("Known Names (Unique IDs for Images):", known_names)