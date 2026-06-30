from django.core.exceptions import ValidationError


def validations(value):
    filesize = value.size
    if filesize > 3000000:
        raise ValidationError('Maximum file size is 3MB.')

def validationRules(value):
    file_size = value.size
    if file_size > 2000000:
        raise ValidationError('Maximum file size is 2MB.') 
