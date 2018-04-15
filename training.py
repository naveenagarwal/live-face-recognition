import face_recognition as fg
import os, json
# from PIL import Image

training_set = {}
ingnore_list = ['.DS_Store', '.', '..']
for entry in os.listdir("training_data"):
    entry_titlize = entry.title()
    if entry in ingnore_list or not os.path.isdir(os.path.join("training_data", entry)):
        continue
    
    profile_path = os.path.join("training_data", entry)
    profile_entries = os.listdir(profile_path)
    
    if entry in profile_entries:
        print("'{}', already trained, so skipping...".format(entry_titlize))
        continue

    print("'{}', Training in progress...".format(entry_titlize))

    for filename in profile_entries:
        if filename.endswith(".jpg"):
            image = fg.load_image_file(os.path.join(profile_path, filename))
            temp_encoding = fg.face_encodings(image)
            if len(temp_encoding) > 0:
                encoding = temp_encoding[0]
                if entry not in training_set:
                    training_set[entry] = []
                training_set[entry].append(encoding.tolist())

    with open(os.path.join(profile_path,entry), "w") as f:
        json.dump({entry_titlize: training_set[entry]}, f)




# for filename in os.listdir("naveen"):
#     if filename.endswith(".jpg"):
#         image = fg.load_image_file(os.path.join("naveen", filename))
#         temp_encoding = fg.face_encodings(image)
#         if len(temp_encoding) > 0:
#             encoding = temp_encoding[0]
#             training_set["naveen"].append(encoding)


# training_set["naveen"] = [obj.tolist() for obj in training_set["naveen"]]

# with open("encoding.txt", "w") as f:
#     json.dump(training_set, f)













# ************ Identify faces and show them in window *****************
# image = fg.load_image_file("training_data/IMG_0986.jpg")
# face_locations = fg.face_locations(image)

# print("total faces {}".format(len(face_locations)))

# i = 1

# for fl in face_locations:
#     top, right, bottom, left = fl

#     face_image = image[top:bottom, left:right]
#     pil_image = Image.fromarray(face_image)
#     pil_image.show()


