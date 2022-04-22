import math
import os

import face_recognition
from matplotlib import pyplot as plt

from api.settings import BASE_DIR
from core.constants import ALLOWED_IMAGES_EXTENSION


def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))


def get_electors_pictures_encodings():
    pictures = []
    pictures_names = []
    pictures_directory = os.path.join(BASE_DIR, "pictures")
    pictures_directory = pictures_directory + os.sep + "electors"
    for root, dirs, files in os.walk(pictures_directory):
        for name in files:
            file = os.path.join(root, name)
            extension = file.split('.')[1] if file and len(file.split('.')) > 0 else 'no_extension'
            if extension in ALLOWED_IMAGES_EXTENSION:
                try:
                    image = face_recognition.load_image_file(file)
                    encoding = face_recognition.face_encodings(image)[0]
                    pictures.append(encoding)
                    pictures_names.append(file)
                except:
                    pass
    return pictures, pictures_names


def compare_pictures(unknown_image):
    try:
        image = face_recognition.load_image_file(unknown_image)
        unknown_encoding = face_recognition.face_encodings(image)[0]
        pictures, pictures_names = get_electors_pictures_encodings()
        face_distances = face_recognition.face_distance(pictures, unknown_encoding)
        face_distance_to_confs = []
        for face_dist in face_distances:
            face_distance_to_confs.append(face_distance_to_conf(face_dist))
        print(face_distances)
        print(face_distance_to_confs)
        plt.plot(face_distance_to_confs, face_distances, label='Test')
        plt.legend()
        plt.show()
    except Exception as ex:
        print(ex)
    pass

compare_pictures('D:\\projets\\python\\elector-recognizer\\gil.jpg')