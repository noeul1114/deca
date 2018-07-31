from django.contrib.auth import get_user
import json

from boards.models import Attachment
from boards.models import Article

from tutorialPoll.settings import MEDIA_URL


class AttachmentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        if request.path == '/summernote/upload_attachment/':
            if request.method == 'POST':

                container = json.loads(response.getvalue().decode("utf-8"))
                files = container['files']
                user = get_user(request)

                for file in files:
                    mod_url = file['url'].replace(MEDIA_URL, '')
                    ATT = Attachment.objects.get(activated=False, file=mod_url)
                    ATT.user = user
                    ATT.article = Article.objects.get(writer=user, published=False)
                    try:
                        ATT.save()
                    except:
                        pass

            else:
                pass
        else:
            pass


        # Code to be executed for each request/response after
        # the view is called.

        return response



