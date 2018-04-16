import face_recognition as fg
import os
import json
import numpy
from PIL import Image
import cv2, time, random

training_set = {}

greeting_list = [
    "How are you doing?",
    "What’s up?, What’s new?",
    "How’s life?",
    "How’s your day going?",
    "Nice to see you",
    "It’s nice to meet you",
    "I like your face."
]

total_greetings = len(greeting_list) - 1

def load_trained_set():
    ingnore_list = ['.DS_Store', '.', '..']
    for entry in os.listdir("training_data"):
        
        if entry in ingnore_list or not os.path.isdir(os.path.join("training_data", entry)):
            continue

        profile_path = os.path.join("training_data", entry)
        profile_entries = os.listdir(profile_path)

        if entry in profile_entries:
            entry_titlize = entry.title()
            print("Found trained set for '{}'. Loading it...".format(entry_titlize))
            
            if entry_titlize not in training_set:
                training_set[entry_titlize] = {
                    "encodings" : [],
                    "greeted" : False,
                    "image_displayed": False
                }
            with open(os.path.join("training_data", entry, entry), "r") as f:
                data = json.load(f)[entry_titlize]
                training_set[entry_titlize]["encodings"] = numpy.array(
                    [numpy.array(arr) for arr in data])
            

def show_face(img):
    face_locations = fg.face_locations(img)

    print("total faces {}".format(len(face_locations)))

    i = 1

    for fl in face_locations:
        top, right, bottom, left = fl

        face_image = img[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()
        i = i + 1


def show_face_at_location(img, location):
    face_locations = fg.face_locations(img)

    fl = face_locations[location]
    top, right, bottom, left = fl

    face_image = img[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()


# Check from training set if a person exists or not.

def compare_and_show(unknown_image):
    temp_encoding = fg.face_encodings(unknown_image) 
    
    if len(temp_encoding) < 1:
        return True
    temp_encoding = [temp_encoding[0]]
    for entry_titlize in training_set:
        print("Checking for profile {}".format(entry_titlize))
        count = 0
        
        for unknown_encoding in temp_encoding:
            result = fg.compare_faces(
                training_set[entry_titlize]["encodings"], unknown_encoding)
            print(result)
            result = [result[0]]
            if True in result and not training_set[entry_titlize]["image_displayed"]:
                
                show_face_at_location(unknown_image, count)
                # training_set[entry_titlize]["image_displayed"] = True

                if not training_set[entry_titlize]["greeted"]:
                    greetings = greeting_list[random.randint(0,total_greetings)]
                    os.system(
                        "say 'Welcome {}, {}'".format(entry_titlize, greetings))
                    # training_set[entry_titlize]["greeted"] = True

            count = count + 1

def lets_go():
    load_trained_set()
    process_this_frame = True

    while True:

        # Get a reference to webcam #0 (the default one)
        try:
            video_capture = cv2.VideoCapture(0)
            # Grab a single frame of video
            ret, frame = video_capture.read()
            # Resize frame of video to 1/4 size for faster face recognition processing
            # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            small_frame = cv2.resize(frame, (0, 0), fx=0.99, fy=0.99)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            # rgb_small_frame = small_frame[:, :, ::-1]
            rgb_frame = frame[:, :, ::-1]
            
            if process_this_frame:
                # compare_and_show(rgb_small_frame)
                compare_and_show(rgb_frame)

            
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            time.sleep(1)
        finally:
            print("releasing video handler")
            video_capture.release()
        
        # cv2.destroyAllWindows()
    

lets_go()
