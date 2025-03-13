import face_recognition
import numpy as np
from PIL import Image
import os
import cv2
import uuid
import hashlib
def generate_random_id(image: np.ndarray):
    _, buffer = cv2.imencode('.jpeg', image)  # Convert the image to a byte format 
    image_bytes = buffer.tobytes()  
    image_hash = hashlib.sha256(image_bytes).hexdigest()
    image_id = uuid.uuid5(uuid.NAMESPACE_DNS, image_hash)
    return str(image_id)

def load_known_faces():
    known_faces = []
    known_names = []
    images_path=[]
    path="/Users/bhavik/Desktop/face_recognition_fastapi/faces"
    for filename in os.listdir(path):
        imagepath = os.path.join(path, filename)
        if group_photo_path == imagepath:
            continue
        person_image = face_recognition.load_image_file(imagepath)
        face_encodings = face_recognition.face_encodings(person_image)
        if  face_encodings:
            person_encoding = face_encodings[0]
            known_faces.append(person_encoding)
            known_names.append(generate_random_id(person_image) ) 
            images_path.append(filename)
      
    return known_faces, known_names, images_path

def get_face_encodings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    # print("face_encodings/////////////////////////",face_encodings)
    return face_encodings


def recognize_faces_in_group(image_encodings, known_faces, known_names,images_path):
    recognized_people = []
    seen_hashes = set() 
    face_path = "/Users/bhavik/Desktop/face_recognition_fastapi/faces"
    face_locations = face_recognition.face_locations(image)
    # print(image)
    for face_encoding in image_encodings:
        # print(len(image_encodings))
        matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.6)
        # print('known_faces''''''''''''',known_faces)
        # print('face_encoding>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',face_encoding)
        # print('matches........',matches)
        
        if True in matches:  
            first_match_index = matches.index(True)
            # print(first_match_index)
            recognized_people.append((known_names[first_match_index], images_path[first_match_index])) 
            continue
        else:
            # for (top, right, bottom, left) in face_locations:
            #     # print(face_locations)
            #     # unmatched_face = image[top+40:bottom-20, left-6:right+6]
            #     unmatched_face = image[top:bottom,left:right]
            #     image_hash = generate_random_id(unmatched_face)
            #     # cv2.imshow(f"{unmatched_face}", unmatched_face)
            #     # print("detect")
            #     if image_hash not in seen_hashes:
            #         # print('sen...............',seen_hashes)
            #         seen_hashes.add(image_hash)
            #         unmatched_face_filename = os.path.join(face_path, f"unmatched_face_{image_hash}.jpg")
            #         cv2.imwrite(unmatched_face_filename, unmatched_face)
            #         recognized_people.append((image_hash, unmatched_face_filename))
            #         # cv2.waitKey(0)
            #         print(f"Saved unmatched face to {unmatched_face_filename}")
            #     else:
            #         print(f"Face already processed, skipping duplicate: {image_hash}")
            for (top, right, bottom, left) in face_locations:
                unmatched_face = image[top:bottom, left:right]
                image_hash = generate_random_id(unmatched_face)
                if image_hash not in seen_hashes:
                    seen_hashes.add(image_hash)
                    unmatched_face_filename = os.path.join(face_path, f"unmatched_face_{image_hash}.jpg")
                    cv2.imwrite(unmatched_face_filename, unmatched_face)
                    recognized_people.append((image_hash, unmatched_face_filename))
                    print(f"Saved unmatched face to {unmatched_face_filename}")
                else:
                    print(f"Face already processed, skipping duplicate: {image_hash}")
    
    
    print('..............................................................',recognized_people)      
    return recognized_people
    # print("recognize_faces_in_group",recognized_people)
    # return recognized_people

def recognize_faces_in_group_photo(group_photo_path):
    known_faces, known_names,images_path = load_known_faces()
    image_encodings = get_face_encodings(group_photo_path)

    if len(image_encodings) == 0:
        print("No faces found in the image.")
        return []

    
    recognized_people = recognize_faces_in_group(image_encodings, known_faces, known_names,images_path)

    if not recognized_people:
        print("No recognized faces found in the image.")
        return []
    print('recognize_faces_in_group_photo',recognized_people)
    return recognized_people


# Main execution
def main(group_photo_path_1):
    global group_photo_path
    group_photo_path = group_photo_path_1
    face_path = "/Users/bhavik/Desktop/face_recognition_fastapi/faces"
    
    global image
    image = cv2.imread(group_photo_path)
    
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image, number_of_times_to_upsample=1, model="hog")
    recognized_people = recognize_faces_in_group_photo(group_photo_path)
    print("recognized_people", recognized_people)
    for index, (top, right, bottom, left) in enumerate(face_locations):
            # name, image_path = recognized_people[index]
            #  cv2.rectangle(image, (left-6, top-40), (right+6, bottom+20), (255, 0, 0), 2)
        cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
        face_image = image[top:bottom, left:right]
            # pil_image = Image.fromarray(face_image)
            # face_filename = os.path.join(face_path, f"face_{index}.jpg")
            # pil_image.save(face_filename)
            # print(pil_image)
        # cv2.imshow(f"{index}", face_image)
        # cv2.waitKey(0)
    # cv2.imshow("Group Image with Faces", image)
    # cv2.waitKey(0)
    return recognized_people


    
    

   








