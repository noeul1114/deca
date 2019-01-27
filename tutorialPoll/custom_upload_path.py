import os
from datetime import datetime
import uuid
import posixpath


def custom_uploaded_filepath_debug(instance, filename):
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


def custom_uploaded_filepath_deploy(instance, filename):
    """
    Returns default filepath for uploaded files.
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')
    hour = datetime.now().strftime('%H')
    return posixpath.join('django-summernote', year, month, day, hour, filename)


def custom_uploaded_filepath_debug_board_image(instance, filename):
    """
    Returns default filepath for uploaded files.
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')
    hour = datetime.now().strftime('%H')
    return os.path.join('board_image', year, month, day, hour, filename)


def custom_uploaded_filepath_deploy_board_image(instance, filename):
    """
    Returns default filepath for uploaded files.
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')
    hour = datetime.now().strftime('%H')
    return posixpath.join('board_image', year, month, day, hour, filename)


def custom_uploaded_filepath_debug_thumb_image(instance, filename):
    """
    Returns default filepath for uploaded files.
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')
    hour = datetime.now().strftime('%H')
    return os.path.join('article_image_thumb', year, month, day, hour, filename)


def custom_uploaded_filepath_deploy_thumb_image(instance, filename):
    """
    Returns default filepath for uploaded files.
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')
    hour = datetime.now().strftime('%H')
    return posixpath.join('article_image_thumb', year, month, day, hour, filename)