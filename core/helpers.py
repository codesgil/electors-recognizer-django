import base64
import datetime
import io
import math
import os
import time

import face_recognition
from PIL import Image

from api.settings import BASE_DIR
from api.settings import UPLOAD_DIR
from globals.utils import send_sms
from .constants import ALLOWED_IMAGES_EXTENSION, FACE_PRECISION


def decode_base64_file(data):
    def get_file_extension(file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    from django.core.files.base import ContentFile
    import base64
    import six
    import uuid

    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = "%s.%s" % (file_name, file_extension,)

        return ContentFile(decoded_file, name=complete_file_name)


def get_image_from_data_url(image_content):
    decodedbytes = base64.decodebytes(str.encode(image_content))
    image_stream = io.BytesIO(decodedbytes)
    image = Image.open(image_stream)
    return image


def handle_uploaded_file(f, directory=UPLOAD_DIR, extra_date_folder=True):
    day_directory = directory
    if extra_date_folder:
        day_directory = day_directory + os.sep + datetime.datetime.today().strftime('%Y-%m-%d')
    if not os.path.exists(day_directory):
        os.makedirs(day_directory, exist_ok=True)
    filename = day_directory + os.sep + str(time.time()).replace('.', '') + '.' + str(f.name).split('.')[1]
    if not os.path.exists(filename):
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    return filename


def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))


def get_best_face_distance(items):
    great = items[0]
    index = 0
    for pos, item in enumerate(items):
        if great < item:
            great = item
            index = pos
    return index, great


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


def get_elector_pictures(matricule):
    pictures_directory = os.path.join(BASE_DIR, "pictures")
    pictures_directory = pictures_directory + os.sep + "electors"
    pictures = []
    for root, dirs, files in os.walk(pictures_directory):
        root_dirs = root.split(os.sep)
        root_matricule = root_dirs[-1]
        if root_matricule == matricule:
            for name in files:
                file = os.path.join(root, name)
                extension = file.split('.')[1] if file and len(file.split('.')) > 0 else 'no_extension'
                if extension in ALLOWED_IMAGES_EXTENSION:
                    pictures.append(name)
    return pictures if pictures else None


def compare_pictures(unknown_image):
    directory_name = None
    file_name = None
    matricule = None
    try:
        image = face_recognition.load_image_file(unknown_image)
        unknown_encoding = face_recognition.face_encodings(image)[0]
        pictures, pictures_names = get_electors_pictures_encodings()
        face_distances = face_recognition.face_distance(pictures, unknown_encoding)
        face_distance_to_confs = []
        for face_dist in face_distances:
            face_distance_to_confs.append(face_distance_to_conf(face_dist))
        print(face_distance_to_confs)
        best_index, best_face_distance = get_best_face_distance(face_distance_to_confs)
        if best_face_distance >= FACE_PRECISION:
            files = pictures_names[best_index].split(os.sep)
            file_name = files[-1]
            matricule, directory_name = get_matricule_directory_in_folder(files)
    except Exception as ex:
        print(ex)
        pass
    return directory_name, file_name, matricule


def get_matricule_directory_in_folder(files):
    try:
        directory = files[-2]
        matricule = files[-2]
        if '-' in matricule:
            matricule = files[-3]
            directory = files[-3] + '/' + directory
    except:
        matricule = files[-2]
        directory = files[-2]
    return matricule, directory


def send_mt(elector):
    from .constants import ACTIVATE_MT, MT_SENDER, MT_MESSAGE
    if ACTIVATE_MT:
        phone = elector.phone
        if phone:
            data = {'name': elector.name}
            message = MT_MESSAGE.format(**data)
            send_sms(content=message, sender=MT_SENDER, phone=phone)
