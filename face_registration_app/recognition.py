import face_recognition
import cv2
import os
from picamera import PiCamera
from picamera.array import PiRGBArray
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

# if __name__ == "__main__":
#     video_capture = cv2.VideoCapture("http://discpi.local:8000/stream.mjpg")
#     known_faces, face_names = load_known_faces("registered_faces")
    
#     while True:
#         ret, frame = video_capture.read()
#         identify_faces(frame, known_faces, face_names)
#         cv2.imshow("Face Recognition", frame)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break

#     video_capture.release()
#     cv2.destroyAllWindows()
if __name__ == "__main__":
    # Initialize the PiCamera
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    raw_capture = PiRGBArray(camera, size=(640, 480))

    known_faces, face_names = load_known_faces("registered_faces")

    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):

        identify_faces(frame.array, known_faces, face_names)
        cv2.imshow("Face Recognition", frame.array)


        raw_capture.truncate(0)  # Clear the buffer

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
