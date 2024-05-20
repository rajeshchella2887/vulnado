from authorization.apis import get_group_details, get_organization_details, get_organization_tree, get_user_details
from connectors import apis
from dashboards.apis import get_users
from datatable_ajax_request_parser.django_extension import DjangoDTResponse, get_django_datatable_query
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.views.generic import View
from ntt_portal_library.contracts.api_contracts.roles.get_group_details_contract import GetGroupDetailsDataDomain
from ntt_portal_library.contracts.api_contracts.roles.get_organization_details_contract import (
    GetOrganizationDetailsDataDomain,
)
from ntt_portal_library.contracts.api_contracts.roles.get_user_details_contract import GetUserDetailsDataDomain
from providers.apis import get_providers
from utils.mixins.view_mixins import NTTDefaultLoginRequiredMixin


class AjaxGetProvidersView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        parsed_query = get_django_datatable_query(raw_request=request.build_absolute_uri())

        success, response = get_providers(request, parsed_query)
        if success:
            self.inject_additional_template_data(response)
            return JsonResponse(response.convert_to_dt_response_dict())

        return HttpResponseBadRequest()

    def inject_additional_template_data(self, dt_response: DjangoDTResponse):
        results = dt_response.data

        for res in results:
            res["grid_url"] = reverse("services:catalogs", kwargs={"provider_name": res["provider_name"]})
            res["edit_url"] = reverse("providers:update-provider", kwargs={"pk": res["id"]})
            res["delete_url"] = reverse("providers:delete-provider", kwargs={"pk": res["id"]})


class AjaxUserDetailsView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request, username):
        success, response = get_user_details(request, GetUserDetailsDataDomain(name=username))

        if success:
            return JsonResponse([d.to_dict() for d in response.data], safe=False)

        return HttpResponseBadRequest()


class AjaxGroupDetailsView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request, group_name):
        success, response = get_group_details(request, GetGroupDetailsDataDomain(name=group_name))

        if success:
            return JsonResponse([d.to_dict() for d in response.data], safe=False)

        return HttpResponseBadRequest()


class AjaxOrganizationDetailsView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request, org_name):
        success, response = get_organization_details(request, GetOrganizationDetailsDataDomain(name=org_name))

        if success:
            return JsonResponse([d.to_dict() for d in response.data], safe=False)

        return HttpResponseBadRequest()


class AjaxOrganizationTreeView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request):
        success, response = get_organization_tree(request)

        if success:
            # NOTE: https://stackoverflow.com/questions/25963552/json-response-list-with-django
            # NOTE: https://stackoverflow.com/questions/62602371/django-jsonresponse-with-safe-false-to-d3
            return JsonResponse([d.to_dict() for d in response.data], safe=False)

        return HttpResponseBadRequest()


class AjaxIncidentsSlaGraphView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request):
        success, response = apis.get_itsm_graph_calculations(request)
        graph_values = response.data

        if success:
            return JsonResponse([d.to_dict() for d in graph_values], safe=False)

        return HttpResponseBadRequest()


class AjaxIncidentsDataTableView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        parsed_query = get_django_datatable_query(raw_request=request.build_absolute_uri())
        success, itsm_incident_list = apis.get_incidents_list(request, parsed_query)
        if success:
            self.additional_template_incident_data(itsm_incident_list)
            return JsonResponse(itsm_incident_list.convert_to_dt_response_dict())

        return HttpResponseBadRequest()

    def additional_template_incident_data(self, dt_response: DjangoDTResponse):
        pass  # pass


class AjaxIncidentDashboardView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        parsed_query = get_django_datatable_query(raw_request=request.build_absolute_uri())
        success, response = apis.get_incidents_dashboard_view(request, parsed_query)

        if success:
            self.additional_incident_data(response)
            return JsonResponse(response.convert_to_dt_response_dict())

        return HttpResponseBadRequest()

    def additional_incident_data(self, dt_response: DjangoDTResponse):
        pass  # pass


class AjaxGetUsersView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        parsed_query = get_django_datatable_query(raw_request=request.build_absolute_uri())

        success, response = get_users(request, parsed_query)

        if success:
            self.inject_additional_template_data(response)
            return JsonResponse(response.convert_to_dt_response_dict())

        return HttpResponseBadRequest()

    def inject_additional_template_data(self, dt_response: DjangoDTResponse):
        results = dt_response.data

        for res in results:
            res["edit_url"] = reverse("accounts:update_user", kwargs={"user_id": res["id"]})
            res["delete_url"] = reverse("accounts:delete-user", kwargs={"pk": res["id"]})
