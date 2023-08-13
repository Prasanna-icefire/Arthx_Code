import cv2
import os
import face_recognition
import time

def register_new_face(frame, name, output_folder):
    output_path = os.path.join(output_folder, f"{name}.jpg")
    cv2.imwrite(output_path, frame)

    print(f"Registered new face: {name}")

def start_registration(name):
    #name = input("Enter name for the new face: ")
    output_folder = "registered_faces"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_capture = cv2.VideoCapture(0)
    start_time = time.time()
    while True:
        ret, frame = video_capture.read()
        #cv2.imshow("Capture Face", frame)

        key = cv2.waitKey(1)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        if(time.time()-start_time>10):
            register_new_face(frame,name,output_folder)
            break
    video_capture.release()
    cv2.destroyAllWindows()

#start_registration()