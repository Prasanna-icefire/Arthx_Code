from cv2 import VideoCapture
import face_recognition
import cv2
import os
import time

def load_known_faces(folder):
    known_faces = []
    face_names = []

    for filename in os.listdir(folder):
        name = os.path.splitext(filename)[0]
        face_image = face_recognition.load_image_file(os.path.join(folder, filename))
        face_encoding = face_recognition.face_encodings(face_image)[0]
        known_faces.append(face_encoding)
        face_names.append(name)

    return known_faces, face_names

def identify_faces(frame, known_faces, face_names):
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"

        if any(matches):
            index = matches.index(True)
            name = face_names[index]

        top, right, bottom, left = face_locations[0]
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

def recognise():
    video_capture = cv2.VideoCapture(0)

    known_faces, face_names = load_known_faces("registered_faces")
    video_capture.set(cv2.CAP_PROP_FPS, 5)
    video_capture.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
    


    while True:

        ret, frame = video_capture.read()
        identify_faces(frame, known_faces, face_names)
        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()
