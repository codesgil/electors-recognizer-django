from django.utils.translation import ugettext_lazy as _

MT_MESSAGE = "M/Mme/Mlle. {name} votre vote a été pris en compte."
MT_SENDER = 'myVote'
ACTIVATE_MT = True
ALLOWED_IMAGES_EXTENSION = ['jpg', 'jpeg']
OPERATION_ACCESS = 'ACCESS'
OPERATION_CONFIRM = 'CONFIRM'
FACE_PRECISION = 0.8

OPERATIONS = (
    (OPERATION_ACCESS, _(OPERATION_ACCESS)),
    (OPERATION_CONFIRM, _(OPERATION_CONFIRM)),
)
