import os
import datetime
import uuid

def custom_uploaded_filepath(instance, filename):
    """
    Returns default filepath for uploaded files.
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')
    hour = datetime.now().strftime('%H')
    return os.path.join('django-summernote', year, month, day, hour, filename)