import json
from typing import List, Tuple

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView
from ntt_portal_library.contracts.api_contracts.jobs.get_job_contract import GetJobDataDomain
from ntt_portal_library.contracts.api_contracts.jobs.get_job_output_contract import GetJobOutputDataDomain
from ntt_portal_library.contracts.api_contracts.jobs.get_job_status_contract import GetJobStatusDataDomain
from ntt_portal_library.contracts.api_contracts.jobs.post_jobs_contract import PostJobDataDomain
from services.apis import (
    GetCatalogsDataDomain,
    get_ansible_job,
    get_catalogs,
    get_credentials_list,
    get_inventories_list,
    get_launch_ansible_job_status,
    get_launch_job_output,
    get_launch_job_response,
)
from services.forms import LaunchJobForm
from utils.mixins.view_mixins import NTTDefaultLoginRequiredMixin, SegmentBreadCrumbEnabledMixin


# Create your views here.
class BaseViewMixin(NTTDefaultLoginRequiredMixin, SegmentBreadCrumbEnabledMixin):
    pass


class GetCatalogsView(BaseViewMixin, TemplateView):
    template_name = "services/ansible/get_catalogs.html"
    provider_name: str = None

    @property
    def segment(self) -> str:
        return "Service Catalogs"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("providers", reverse("dashboards:providers")),
            (
                "catalogs",
                reverse("services:catalogs", kwargs={"provider_name": self.provider_name}),
            ),
        ]

    def get(self, request, provider_name):
        self.provider_name = provider_name

        page = request.GET.get("page")
        page_size = request.GET.get("page_size")
        search = request.GET.get("search")
        current_path = request.path

        success, response = get_catalogs(
            request,
            GetCatalogsDataDomain(
                page=page,
                page_size=page_size,
                search=search,
                provider=self.provider_name,
            ),
        )

        context = super().get_context_data()

        if success:
            page_obj = response.data
            catalogs = response.data.results

            context.update(
                {
                    "catalogs": catalogs,
                    "provider": self.provider_name,
                    "page_obj": page_obj,
                    "current_page_num": page_obj.current_page,
                    "previous_page_num": page_obj.current_page - 1,
                    "next_page_num": page_obj.current_page + 1,
                    "total_pages": page_obj.total_pages,
                    "page_range": page_obj.page_range,
                    "last_page_num": page_obj.page_range[-1],
                    "page_size": page_size,
                    "search": search,
                    "refresh_url_paginate": current_path,
                }
            )

            return render(request, self.template_name, context)
        else:
            return redirect(reverse("dashboards:providers"))


# baseUpdateView, UpdateView, breaks
class LaunchAnsibleJobView(BaseViewMixin, ProcessFormView):
    form_class = LaunchJobForm
    template_name = "services/ansible/launch_job.html"
    provider_hostname: str = None
    provider_id: int = None
    provider_name: str = None
    template_id: int = None

    @property
    def segment(self) -> str:
        return "Service Catalogs"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("providers", reverse("dashboards:providers")),
            (
                "catalogs",
                reverse("services:catalogs", kwargs={"provider_name": self.provider_name}),
            ),
            (
                self.template_id,
                reverse(
                    "services:launch_job",
                    kwargs={"pk": self.template_id, "provider_name": self.provider_name},
                ),
            ),
        ]

    def get(self, request, pk, provider_name, *args, **kwargs):
        # NOTE: used for path_to_current_view to pass pk to the frontend
        self.provider_name = provider_name
        self.template_id = pk
        success, response = get_ansible_job(request, GetJobDataDomain(template_id=int(self.template_id)))

        if not success:
            return redirect(reverse("dashboards:providers"))

        # get inventories, credentials via microservice to populate options
        inventory_resp_success, inventory_resp = get_inventories_list(request)
        credentials_resp_success, credentials_resp = get_credentials_list(request)

        get_ansible_job_resp_data_dict = response.data.to_dict().copy()

        if not inventory_resp_success or not credentials_resp_success:
            form = self.form_class(initial=get_ansible_job_resp_data_dict)
            context = {
                **self.get_context_data(form=form),
                "type": inventory_resp.type + credentials_resp.type,
                "errors": inventory_resp.errors + credentials_resp.errors,
            }

            return render(request, self.template_name, context=context)

        get_ansible_job_resp_data_dict["template_id"] = self.template_id
        get_ansible_job_resp_data_dict["inventory"] = inventory_resp.data.to_dict().get("results", None)
        get_ansible_job_resp_data_dict["credentials"] = credentials_resp.data.to_dict().get("results", None)

        form = self.form_class(
            initial=get_ansible_job_resp_data_dict,
            parsed_extra_vars=response.data.parsed_extra_vars,
            choice_data=get_ansible_job_resp_data_dict,
        )

        context = {
            **self.get_context_data(form=form),
            "provider_name": provider_name,
            "name": response.data.name,
            "type": response.data.type,
            "template_id": self.template_id,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, pk, provider_name):
        self.template_id = pk
        self.provider_name = provider_name

        query_dict = request.POST
        mutable_post = query_dict.copy()

        exclude_keys = [
            "csrfmiddlewaretoken",
            "credentials",
            "inventory",
            "launch_url",
            "provider",
            "submit",
            "parsed_extra_vars",
        ]
        extra_vars = {key: value for key, value in mutable_post.items() if key not in exclude_keys}
        mutable_post["parsed_extra_vars"] = json.dumps(extra_vars)

        for key in extra_vars:
            if key in mutable_post:
                del mutable_post[key]

        form = self.form_class(data=mutable_post, initial={"template_id": pk})

        if form.is_valid():
            return self.handle_form_valid(request, form)

        return render(request, self.template_name, self.get_context_data(form=form))

    def handle_form_valid(self, request, form):
        launch_url = form.cleaned_data["launch_url"]
        payload = {
            "credential": form.cleaned_data["credentials"],
            "extra_vars": form.cleaned_data["parsed_extra_vars"],
            "inventory": form.cleaned_data["inventory"],
        }
        parsed_extra_vars = form.cleaned_data.get("parsed_extra_vars", {})
        template_id = form.cleaned_data["template_id"]
        cleaned_data = form.cleaned_data
        parsed_extra_vars = cleaned_data.get("parsed_extra_vars", {})
        temp_id = {"template_id": template_id}

        success, response = get_launch_job_response(
            request,
            PostJobDataDomain(template_id=template_id, launch_url=launch_url, payload=payload),
        )
        form = self.form_class(initial=temp_id, parsed_extra_vars=parsed_extra_vars)
        if success:
            context = {}
            if type(response.data) is dict:
                response_data = response.data
                context = {
                    **self.get_context_data(form=form),
                    "name": response_data["name"],
                    "template_id": response_data["summary_fields"]["unified_job_template"]["id"],
                    "job_id": response_data["id"],
                    "status": response_data["status"].capitalize(),
                    "status_url": response_data["url"],
                    "stdout_url": response_data["related"]["stdout"],
                    "traceback_result": response_data["result_traceback"],
                    "parsed_extra_vars": parsed_extra_vars,
                }
            else:
                context = {
                    **self.get_context_data(form=form),
                    "name": response.data.name,
                    "template_id": response.data.summary_fields["unified_job_template"]["id"],
                    "job_id": response.data.id,
                    "status": response.data.status.capitalize(),
                    "status_url": response.data.url,
                    "stdout_url": response.data.related["stdout"],
                    "traceback_result": response.data.result_traceback,
                    "parsed_extra_vars": parsed_extra_vars,
                }
            return render(request, self.template_name, context=context)
        else:
            return render(
                request,
                self.template_name,
                self.get_context_data(form=form, errors=response.errors),
            )


class GetAnsibleJobStatusView(View):
    def get(self, request, *args, **kwargs):
        status_url = request.GET.get("status_url")
        template_id = request.GET.get("template_id")
        job_id = request.GET.get("job_id", None)
        success, response = get_launch_ansible_job_status(
            request,
            GetJobStatusDataDomain(template_id=template_id, status_url=status_url, job_id=job_id),
        )
        response_data = response.data

        if success:
            return JsonResponse(response_data)

        return HttpResponseBadRequest(response)


class GetAnsibleJobOutputView(View):
    def get(self, request, *args, **kwargs):
        job_uuid = request.GET.get("job_uuid")
        template_id = request.GET.get("template_id")

        success, response = get_launch_job_output(
            request, GetJobOutputDataDomain(template_id=template_id, job_uuid=job_uuid)
        )

        if success:
            return HttpResponse(response.data)

        return HttpResponseBadRequest(response)


class JobsListView(BaseViewMixin, TemplateView):
    template_name = "services/jobs/jobs_list.html"

    @property
    def segment(self) -> str:
        return "Jobs List"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            (
                "jobs_list",
                reverse("services:jobs_list"),
            ),
        ]

    def get(self, request):
        context = super().get_context_data()
        return render(request, self.template_name, context)


class JobDetailsView(BaseViewMixin, TemplateView):
    template_name = "services/jobs/job_details.html"

    @property
    def segment(self) -> str:
        return "Job Details"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            (
                "jobs_list",
                reverse("services:jobs_list"),
            ),
            (
                "job_details",
                reverse(
                    "services:jobdetails",
                ),
            ),
        ]

    def get(self, request):
        context = super().get_context_data()
        return render(request, self.template_name, context)


class FormView(BaseViewMixin, TemplateView):
    template_name = "services/form/form.html"

    @property
    def segment(self) -> str:
        return "form"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            (
                "form",
                reverse("services:form"),
            ),
        ]

    def get(self, request):
        context = super().get_context_data()
        return render(request, self.template_name, context)


class ConfigPlanView(BaseViewMixin, TemplateView):
    template_name = "services/remediation/configplan.html"

    @property
    def segment(self) -> str:
        return "configplan"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            (
                "configplan",
                reverse("services:configplan"),
            )
        ]

    def get(self, request):
        context = super().get_context_data()
        return render(request, self.template_name, context)
