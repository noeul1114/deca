from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.conf import settings
from django.template import Template, Context

import json

from django.http import JsonResponse

from boards.models import Attachment
from boards.models import Article


class AttachmentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     print(request, view_args, view_func, view_kwargs)
    #     response = None
    #     return response


