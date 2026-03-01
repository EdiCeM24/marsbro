from django.core.exceptions import ValidationError


def validations(value):
  filesize = value.size
  if filesize > 4000000:
    raise ValidationError('Maximum file size is 4MB.')
  
def validationRules(value):
  file_size = value.size
  if file_size > 2000000:
    raise ValidationError('Maximum file size is 2MB.')  
  

