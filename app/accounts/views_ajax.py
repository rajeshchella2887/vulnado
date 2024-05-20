from accounts.apis import get_ldap_settings
from datatable_ajax_request_parser.django_extension import DjangoDTResponse, get_django_datatable_query
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.views import View
from utils.mixins.view_mixins import NTTDefaultLoginRequiredMixin


class AjaxGetLDAPSettingsView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        parsed_query = get_django_datatable_query(raw_request=request.build_absolute_uri())

        success, response = get_ldap_settings(request, parsed_query)
        if success:
            self.inject_additional_template_data(response)
            return JsonResponse(response.convert_to_dt_response_dict())

        return HttpResponseBadRequest()

    def inject_additional_template_data(self, dt_response: DjangoDTResponse):
        results = dt_response.data

        for res in results:
            res["edit_url"] = reverse("accounts:update_ldap_settings", kwargs={"pk": res["id"]})
            res["delete_url"] = reverse("accounts:delete_ldap_settings", kwargs={"pk": res["id"]})
