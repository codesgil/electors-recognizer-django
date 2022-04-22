import os
from django import forms
from django.core.exceptions import ValidationError
from .constants import ALLOWED_IMAGES_EXTENSION


class TextFileField(forms.ImageField):
    def validate(self, value):
        # First run the parent class' validation routine
        super().validate(value)
        # Run our own file extension check
        file_extension = str(os.path.splitext(value.name)[1]).replace('.', '')
        if not (file_extension in ALLOWED_IMAGES_EXTENSION):
            raise ValidationError(
                ('Invalid file extension'),
                code='invalid'
            )
