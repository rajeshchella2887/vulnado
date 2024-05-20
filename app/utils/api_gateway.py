from django.conf import settings
from ntt_portal_library.helpers.api_utils import RequestsWrapper

api_gateway = RequestsWrapper(host=settings.AUTH_SERVICE_HOST, debug=settings.DEBUG)
