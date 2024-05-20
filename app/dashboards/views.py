from typing import List, Tuple

from connectors import apis, enums
from dashboards.apis import get_user
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.generic import TemplateView
from ntt_portal_library.contracts.api_contracts.accounts.get_user_contract import GetUserDataDomain
from utils.mixins.view_mixins import NTTDefaultLoginRequiredMixin, SegmentBreadCrumbEnabledMixin


class DashboardIndexView(NTTDefaultLoginRequiredMixin, TemplateView):
    template_name = "dashboard-index.html"


class ProvidersView(NTTDefaultLoginRequiredMixin, TemplateView, SegmentBreadCrumbEnabledMixin):
    template_name = "dashboards/providers.html"

    @property
    def segment(self) -> str:
        return "Providers Dashboard"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("providers", reverse("dashboards:providers")),
        ]


class AuthorizationView(NTTDefaultLoginRequiredMixin, TemplateView, SegmentBreadCrumbEnabledMixin):
    template_name = "dashboards/authorization.html"

    @property
    def segment(self) -> str:
        return "Authorization Dashboard"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("authorization", reverse("dashboards:authorization")),
        ]


class ConnectorsView(NTTDefaultLoginRequiredMixin, TemplateView, SegmentBreadCrumbEnabledMixin):
    template_name = "dashboards/connectors.html"

    @property
    def segment(self) -> str:
        return "ServiceNow Dashboard"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("ServiceNow", reverse("dashboards:connectors")),
        ]

    def get(self, request: HttpRequest, *args, **kwargs):
        success, itsm_incidents_list = apis.get_incidents(request)
        itsm_incidents_json = itsm_incidents_list.data

        success, calculation_response = apis.get_itsm_dashboard_calculations(request)
        dashboard_values = calculation_response.data
        total_incidents_count = dashboard_values.get("total_incidents_count")
        open_incidents = dashboard_values.get("open_incidents_count")
        in_progress_incidents = dashboard_values.get("in_progress_incidents_count")
        on_hold_incidents = dashboard_values.get("on_hold_incidents_count")
        closed_incidents = dashboard_values.get("closed_incidents_count")
        open_incidents_thirty_days = dashboard_values.get("open_incidents_thirty_days_count")
        date_thirty_days = dashboard_values.get("date_thirty_days")
        current_date = timezone.now().strftime("%B %d, %Y")
        date_seven_days = dashboard_values.get("date_seven_days")
        unassigned_incidents_count = dashboard_values.get("unassigned_incidents_count")
        incident_not_updated_seven_days_count = dashboard_values.get("incident_not_updated_seven_days_count")

        success, response = apis.get_itsm_graph_calculations(request)
        graph_datas = response.data
        sla_graph_data = graph_datas.get("sla_graph_results")
        x_axis = []
        y_axis_value_yes = []
        y_axis_value_no = []
        for item in sla_graph_data:
            x_axis_data = "0000" if item["sla_due_date"] is None else item["sla_due_date"]
            x_axis.append(x_axis_data)
            y_axis_yes_value = item["inc_count"] if item["condition"] is True else 0
            y_axis_value_yes.append(y_axis_yes_value)
            y_axis_no_value = item["inc_count"] if item["condition"] is False else 0
            y_axis_value_no.append(y_axis_no_value)
        x_axis_data_count = x_axis
        y_axis_yes_value_list = y_axis_value_yes
        y_axis_no_value_list = y_axis_value_no
        y_axis_true = enums.SlaStateEnum.YES.value
        y_axis_false = enums.SlaStateEnum.NO.value

        success, priority_chart_response = apis.get_itsm_priority_chart_calculations(request)
        priority_chart_datas = priority_chart_response.data
        priority_data = priority_chart_datas.get("sla_priority_graph_results")
        open_incidents_values = []
        in_progress_incidents_values = []
        closed_incidents_values = []
        unassigned_incidents_values = []
        for value in priority_data:
            open_incidents_data = value["open_incident_count"]
            open_incidents_values.append(open_incidents_data)
            in_progress_data = value["in_progress_incident_count"]
            in_progress_incidents_values.append(in_progress_data)
            closed_incidents_data = value["closed_incident_count"]
            closed_incidents_values.append(closed_incidents_data)
            unassigned_incidents_data = value["unassigned_incident_count"]
            unassigned_incidents_values.append(unassigned_incidents_data)

        chart_open_incidents_count = open_incidents_values
        chart_in_incidents_count = in_progress_incidents_values
        chart_closed_incidents_count = closed_incidents_values
        chart_unassigned_incidents_count = unassigned_incidents_values

        priority_groups_data = []
        for group in enums.PriorityGroupsEnum:
            groups_value = group.value[1]
            priority_groups_data.append(groups_value)

        priority_groups = priority_groups_data
        state_enums = enums.ServiceNowStateEnum

        context = {
            **super().get_context_data(**kwargs),
            "total_incidents_count": total_incidents_count,
            "open_incidents_count": open_incidents,
            "in_progress_incidents_count": in_progress_incidents,
            "on_hold_incidents_count": on_hold_incidents,
            "closed_incidents_count": closed_incidents,
            "open_incidents_thirty_days_count": open_incidents_thirty_days,
            "x_axis_data_count": x_axis_data_count,
            "y_axis_yes_value_list": y_axis_yes_value_list,
            "y_axis_no_value_list": y_axis_no_value_list,
            "date_thirty_days": date_thirty_days,
            "current_date": current_date,
            "y_axis_true": y_axis_true,
            "y_axis_false": y_axis_false,
            "date_seven_days": date_seven_days,
            "unassigned_incidents_count": unassigned_incidents_count,
            "incident_not_updated_seven_days_count": incident_not_updated_seven_days_count,
            "chart_open_incidents_count": chart_open_incidents_count,
            "chart_in_incidents_count": chart_in_incidents_count,
            "chart_closed_incidents_count": chart_closed_incidents_count,
            "chart_unassigned_incidents_count": chart_unassigned_incidents_count,
            "priority_groups": priority_groups,
            "itsm_incidents_json": itsm_incidents_json,
            "state_enums": [state for state in state_enums],
        }
        if success:
            return render(request, "dashboards/connectors.html", context=context)

        return HttpResponseBadRequest()


class AuthenticationView(NTTDefaultLoginRequiredMixin, TemplateView, SegmentBreadCrumbEnabledMixin):
    template_name = "dashboards/authentication.html"

    @property
    def segment(self) -> str:
        return "Authentication Dashboard"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("authentication", reverse("dashboards:authentication")),
        ]


class ComplianceMgtView(NTTDefaultLoginRequiredMixin, TemplateView, SegmentBreadCrumbEnabledMixin):
    template_name = "dashboards/compliance-management.html"

    @xframe_options_sameorigin
    def ok_to_load_in_a_frame(self, request):
        return HttpResponse("This page is safe to load in a frame on any site.")

    @property
    def segment(self) -> str:
        return "Compliance Management Dashboard"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("compliance-management", reverse("dashboards:compliance-management")),
        ]

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {**super().get_context_data(**kwargs)}

        param = request.GET.get("param")
        current_path = request.path

        context.update({"param": param, "refresh_url": current_path})

        return render(request, self.template_name, context)


class AssetMgtView(NTTDefaultLoginRequiredMixin, TemplateView, SegmentBreadCrumbEnabledMixin):
    template_name = "dashboards/asset-management.html"

    @xframe_options_sameorigin
    def ok_to_load_in_a_frame(self, request):
        return HttpResponse("This page is safe to load in a frame on any site.")

    @property
    def segment(self) -> str:
        return "Asset Management Dashboard"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("asset-management", reverse("dashboards:asset-management")),
        ]


class UsersView(NTTDefaultLoginRequiredMixin, TemplateView, SegmentBreadCrumbEnabledMixin):
    template_name = "dashboards/users.html"

    @property
    def segment(self) -> str:
        return "Users Dashboard"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("users", reverse("dashboards:users")),
        ]

    def get(self, request: HttpRequest, *args, **kwargs):
        logged_in_user = request.user

        success, response = get_user(request, GetUserDataDomain(username=logged_in_user.username))

        if success:
            logged_in_user_groups = response.data.groups

            context = {"logged_in_user_groups": logged_in_user_groups}

            existing_context = super().get_context_data(**kwargs)
            existing_context.update(context)

            return render(request, "dashboards/users.html", existing_context)
