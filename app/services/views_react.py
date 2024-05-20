import json
from typing import List

from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.views import View
from ntt_portal_library.contracts.api_contracts.forms.get_catalog_details_contract import GetCatalogDetailsDataDomain
from ntt_portal_library.contracts.api_contracts.forms.post_os_self_query_contract import PostOSSelfQueryDataDomain
from ntt_portal_library.contracts.api_contracts.jobs.get_job_output_contract import GetJobOutputDataDomain
from ntt_portal_library.contracts.api_contracts.jobs.get_jobs_list_contract import GetJobsListDataDomain
from ntt_portal_library.contracts.api_contracts.jobs.get_provider_type_contract import GetProviderDataDomain
from ntt_portal_library.contracts.api_contracts.jobs.post_jobs_contract import PostJobDataDomain
from services.apis import (
    get_catalog_details_output,
    get_jobs_list,
    get_launch_job_output,
    get_launch_job_response,
    get_os_self_query_output,
    get_os_type_output,
    get_provider_type,
)


class ReactGetJobsListView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        page = request.GET.get("page")
        page_size = request.GET.get("page_size")
        search = request.GET.get("search")
        ordering = request.GET.get("ordering")
        order = request.GET.get("order")

        if order == "desc":
            ordering = "-" + ordering

        success, response = get_jobs_list(
            request,
            GetJobsListDataDomain(page=page, page_size=page_size, search=search, ordering=ordering),
        )

        if success:
            return JsonResponse(response.to_dict())

        return HttpResponseBadRequest()


class ReactGetJobOutputView(View):
    job_uuid: str = None
    template_id: int = None

    def get(self, request, *args, **kwargs):
        self.job_uuid = request.GET.get("job_uuid")
        self.template_id = request.GET.get("template_id")

        success, response = get_launch_job_output(
            request, GetJobOutputDataDomain(job_uuid=self.job_uuid, template_id=self.template_id)
        )

        if success:
            return JsonResponse(response.to_dict())

        return HttpResponseBadRequest(response)


class ReactOSTypeView(View):
    def get(self, request, *args, **kwargs):
        success, response = get_os_type_output(request)

        if success:
            return JsonResponse(response.to_dict())

        return HttpResponseBadRequest(response)


class ReactCatalogDetailsView(View):
    catalog_name: str = None

    def get(self, request, *args, **kwargs):
        self.catalog_name = request.GET.get("catalog_name")
        success, response = get_catalog_details_output(
            request, GetCatalogDetailsDataDomain(catalog_name=self.catalog_name)
        )

        if success:
            return JsonResponse(response.to_dict())

        return HttpResponseBadRequest(response)


class ReactOSSelfQueryView(View):
    os_type: str = None
    selected_fields: List[str] = None
    filter_fields: dict[str, List[str]] = None

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        self.os_type = data["os_type"] if "os_type" in data else ""
        self.selected_fields = data["selected_fields"] if "selected_fields" in data else []
        self.filter_fields = data["filter_fields"] if "filter_fields" in data else {}

        success, response = get_os_self_query_output(
            request,
            PostOSSelfQueryDataDomain(
                os_type=self.os_type, selected_fields=self.selected_fields, filter_fields=self.filter_fields
            ),
        )

        if success:
            return JsonResponse(response.to_dict())

        return HttpResponseBadRequest(response)


class ReactJobLaunchView(View):
    template_id: int = None
    launch_url: str = None
    payload: dict = None

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        self.template_id = data["template_id"] if "template_id" in data else None
        self.launch_url = data["launch_url"] if "launch_url" in data else ""
        self.payload = data["payload"] if "payload" in data else {}

        success, response = get_launch_job_response(
            request, PostJobDataDomain(template_id=self.template_id, launch_url=self.launch_url, payload=self.payload)
        )
        if success:
            if type(response.data) is dict:
                response_data = response.data
                context = {
                    "name": response_data["name"],
                    "template_id": "",
                    "job_id": response_data["id"],
                    "status": response_data["status"],
                    "status_url": "",
                    "stdout_url": "",
                    "traceback_result": "",
                }
            else:
                context = {
                    "name": response.data.name,
                    "template_id": response.data.summary_fields["unified_job_template"]["id"],
                    "job_id": response.data.id,
                    "status": response.data.status.capitalize(),
                    "status_url": response.data.url,
                    "stdout_url": response.data.related["stdout"],
                    "traceback_result": response.data.result_traceback,
                }
            return JsonResponse(context)

        return HttpResponseBadRequest(response)


class ReactProviderTypeView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        self.template_id = data["template_id"] if "template_id" in data else int
        success, response = get_provider_type(request, GetProviderDataDomain(template_id=self.template_id))
        if success:
            context = {"provider_type": response.data}
            return JsonResponse(context)

        return HttpResponseBadRequest(response)
