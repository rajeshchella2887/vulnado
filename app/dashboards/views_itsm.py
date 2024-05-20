from typing import List, Tuple

from connectors import apis, enums
from datatable_ajax_request_parser.django_extension import DjangoDTResponse, get_django_datatable_query
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, View
from ntt_portal_library.contracts.api_contracts.connectors.get_itsm_provider_contract import GetParamDataDomain
from utils.mixins.view_mixins import NTTDefaultLoginRequiredMixin, SegmentBreadCrumbEnabledMixin

DATE_TIME_FORMAT = "%B %d, %Y"


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
        context = {
            **super().get_context_data(**kwargs),
        }

        current_path = request.path

        param = request.GET.get("param")
        success, calculation_response = apis.get_itsm_dashboard_calculations(request, GetParamDataDomain(param=param))

        dashboard_values = calculation_response.data

        total_incidents_count = dashboard_values.get("total_incidents_count")
        open_incidents = dashboard_values.get("open_incidents_count")
        in_progress_incidents = dashboard_values.get("in_progress_incidents_count")
        on_hold_incidents = dashboard_values.get("on_hold_incidents_count")
        resolved_incidents = dashboard_values.get("resolved_incidents_count")
        closed_incidents = dashboard_values.get("closed_incidents_count")
        open_incidents_thirty_days = dashboard_values.get("open_incidents_thirty_days_count")
        date_thirty_days = dashboard_values.get("date_thirty_days")
        current_date = timezone.now().strftime(DATE_TIME_FORMAT)
        date_seven_days = dashboard_values.get("date_seven_days")
        info_title = dashboard_values.get("info_title")
        from_date = dashboard_values.get("from_date")
        middle_symbol = dashboard_values.get("middle_symbol")
        to_date = dashboard_values.get("to_date")
        unassigned_incidents_count = dashboard_values.get("unassigned_incidents_count")
        incident_not_updated_seven_days_count = dashboard_values.get("incident_not_updated_seven_days_count")
        older_incidents_count = dashboard_values.get("older_incidents_count")
        priority_data = dashboard_values.get("sla_priority_graph_results")
        category_data = dashboard_values.get("category_chart_results")

        success, response = apis.get_itsm_graph_calculations(request)
        graph_datas = response.data
        sla_graph_data = graph_datas.get("sla_graph_results")
        x_axis = []
        y_axis_value_yes = []
        y_axis_value_no = []
        for item in sla_graph_data:
            x_axis_data = "00-0000" if item["sla_due_date"] is None else item["sla_due_date"]
            x_axis.append(x_axis_data)
            y_axis_yes_value = item["inc_count_true"]
            y_axis_value_yes.append(y_axis_yes_value)
            y_axis_no_value = item["inc_count_false"]
            y_axis_value_no.append(y_axis_no_value)
        x_axis_data_count = x_axis
        y_axis_yes_value_list = y_axis_value_yes
        y_axis_no_value_list = y_axis_value_no
        y_axis_true = enums.SlaStateEnum.YES.value
        y_axis_false = enums.SlaStateEnum.NO.value

        success, priority_chart_response = apis.get_itsm_priority_chart_calculations(request)
        priority_chart_datas = priority_chart_response.data
        year_data = priority_chart_datas.get("years_data")
        years = []
        for value in year_data:
            years_data = value["sla_due_date"]
            years.append(years_data)
        category_open_incidents_values = []
        category_in_progress_incidents_values = []
        category_closed_incidents_values = []
        category_unassigned_incidents_values = []
        category_values = []
        for categories in category_data:
            open_incidents_category_data = categories["open_incident_category_count"]
            category_open_incidents_values.append(open_incidents_category_data)
            in_progress_incidents_category_data = categories["in_progress_incident_category_count"]
            category_in_progress_incidents_values.append(in_progress_incidents_category_data)
            closed_incidents_category_data = categories["closed_incident_category_count"]
            category_closed_incidents_values.append(closed_incidents_category_data)
            unassigned_incidents_category_data = categories["unassigned_incident_category_count"]
            category_unassigned_incidents_values.append(unassigned_incidents_category_data)
            category_list_data = "Null" if categories["category"] is None else categories["category"]
            category_values.append(category_list_data)
        category_open_incidents_count = category_open_incidents_values
        category_in_progress_incidents_count = category_in_progress_incidents_values
        category_closed_incidents_count = category_closed_incidents_values
        category_unassigned_incidents_count = category_unassigned_incidents_values
        category_values_names = category_values
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

        month_data = []
        for month in enums.MonthlyEnum:
            value = month.value
            month_data.append(value)

        priority_groups = priority_groups_data
        state_enums = enums.ServiceNowStateEnum

        context.update(
            {
                "total_incidents_count": total_incidents_count,
                "open_incidents_count": open_incidents,
                "in_progress_incidents_count": in_progress_incidents,
                "on_hold_incidents_count": on_hold_incidents,
                "resolved_incidents_count": resolved_incidents,
                "closed_incidents_count": closed_incidents,
                "open_incidents_thirty_days_count": open_incidents_thirty_days,
                "x_axis_data_count": x_axis_data_count,
                "y_axis_yes_value_list": y_axis_yes_value_list,
                "y_axis_no_value_list": y_axis_no_value_list,
                "date_thirty_days": date_thirty_days,
                "current_date": current_date,
                "y_axis_true": y_axis_true,
                "y_axis_false": y_axis_false,
                "year_data": years,
                "date_seven_days": date_seven_days,
                "category_open_incidents_count": category_open_incidents_count,
                "category_in_progress_incidents_count": category_in_progress_incidents_count,
                "category_closed_incidents_count": category_closed_incidents_count,
                "category_unassigned_incidents_count": category_unassigned_incidents_count,
                "category_values_names": category_values_names,
                "unassigned_incidents_count": unassigned_incidents_count,
                "incident_not_updated_seven_days_count": incident_not_updated_seven_days_count,
                "older_incidents_count": older_incidents_count,
                "chart_open_incidents_count": chart_open_incidents_count,
                "chart_in_incidents_count": chart_in_incidents_count,
                "chart_closed_incidents_count": chart_closed_incidents_count,
                "chart_unassigned_incidents_count": chart_unassigned_incidents_count,
                "priority_groups": priority_groups,
                "info_title": info_title,
                "from_date": from_date,
                "middle_symbol": middle_symbol,
                "to_date": to_date,
                "state_enums": [state for state in state_enums],
                "month_enums": month_data,
                "param": param,
                "refresh_url": current_path,
            }
        )

        if success:
            return render(request, self.template_name, context=context)

        return HttpResponseBadRequest()


class ProblemMgtView(NTTDefaultLoginRequiredMixin, TemplateView, SegmentBreadCrumbEnabledMixin):
    template_name = "dashboards/problem-management.html"

    @property
    def segment(self) -> str:
        return "Problem Management Dashboard"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("Problem Management", reverse("dashboards:problem-management")),
        ]

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
        }
        current_date = timezone.now().strftime(DATE_TIME_FORMAT)
        current_path = request.path

        param = request.GET.get("param")
        success, prb_calculation_response = apis.get_problem_mgt_dashboard_calculations(
            request, GetParamDataDomain(param=param)
        )
        prb_dashboard_values = prb_calculation_response.data

        total_problems_count = prb_dashboard_values.get("total_problems_count")
        open_problems_count = prb_dashboard_values.get("open_problems_count")
        fix_in_progress_count = prb_dashboard_values.get("fix_in_progress_count")
        assess_problems_count = prb_dashboard_values.get("assess_problems_count")
        root_cause_analysis_count = prb_dashboard_values.get("root_cause_analysis_count")
        resolved_problem_count = prb_dashboard_values.get("resolved_problem_count")
        closed_problem_count = prb_dashboard_values.get("closed_problem_count")
        unassigned_problems_count = prb_dashboard_values.get("unassigned_problems_count")
        prb_not_updated_seven_days_count = prb_dashboard_values.get("prb_not_updated_seven_days_count")
        open_problems_thirty_days_count = prb_dashboard_values.get("open_problems_thirty_days_count")
        date_seven_days = prb_dashboard_values.get("date_seven_days")
        date_thirty_days = prb_dashboard_values.get("date_thirty_days")
        prb_priority_data = prb_dashboard_values.get("prb_priority_graph_results")
        prb_category_data = prb_dashboard_values.get("prb_category_chart_results")
        prb_years_data = prb_dashboard_values.get("years_data")
        info_title = prb_dashboard_values.get("info_title")
        from_date = prb_dashboard_values.get("from_date")
        middle_symbol = prb_dashboard_values.get("middle_symbol")
        to_date = prb_dashboard_values.get("to_date")
        open_prb_priority_values = []
        fix_in_progress_prb_priority_values = []
        closed_prb_priority_values = []
        unassigned_prb_priority_values = []
        for value in prb_priority_data:
            open_prb_priority_data = value["open_prb_priority_count"]
            open_prb_priority_values.append(open_prb_priority_data)
            fix_in_progress_prb_priority_data = value["fix_in_progress_prb_priority_count"]
            fix_in_progress_prb_priority_values.append(fix_in_progress_prb_priority_data)
            closed_prb_priority_data = value["closed_incident_count"]
            closed_prb_priority_values.append(closed_prb_priority_data)
            unassigned_prb_priority_data = value["unassigned_incident_count"]
            unassigned_prb_priority_values.append(unassigned_prb_priority_data)

        chart_open_prb_priority_count = open_prb_priority_values
        chart_fix_in_prb_priority_count = fix_in_progress_prb_priority_values
        chart_closed_prb_priority_count = closed_prb_priority_values
        chart_unassigned_prb_priority_count = unassigned_prb_priority_values

        prb_priority_groups_data = []
        for group in enums.PriorityGroupsEnum:
            groups_value = group.value[1]
            prb_priority_groups_data.append(groups_value)

        prb_category_open_values = []
        prb_category_fix_in_progress_values = []
        prb_category_closed_values = []
        prb_category_unassigned_values = []
        prb_category_values = []
        for categories in prb_category_data:
            open_prb_category_data = categories["open_problem_category_count"]
            prb_category_open_values.append(open_prb_category_data)
            prb_fix_in_progress_category_data = categories["fix_in_progress_problem_count"]
            prb_category_fix_in_progress_values.append(prb_fix_in_progress_category_data)
            closed_prb_category_data = categories["closed_problem_category_count"]
            prb_category_closed_values.append(closed_prb_category_data)
            unassigned_prb_category_data = categories["unassigned_incident_category_count"]
            prb_category_unassigned_values.append(unassigned_prb_category_data)
            prb_category_list_data = "Null" if categories["category"] is None else categories["category"]
            prb_category_values.append(prb_category_list_data)

        prb_month_data = []
        for month in enums.MonthlyEnum:
            value = month.value
            prb_month_data.append(value)

        years = []
        for value in prb_years_data:
            years_data = value["sla_due_date"]
            years.append(years_data)

        prb_priority_groups = prb_priority_groups_data

        context.update(
            {
                "total_problems_count": total_problems_count,
                "open_problems_count": open_problems_count,
                "fix_in_progress_count": fix_in_progress_count,
                "assess_problems_count": assess_problems_count,
                "root_cause_analysis_count": root_cause_analysis_count,
                "resolved_problem_count": resolved_problem_count,
                "closed_problem_count": closed_problem_count,
                "unassigned_problems_count": unassigned_problems_count,
                "prb_not_updated_seven_days_count": prb_not_updated_seven_days_count,
                "open_problems_thirty_days_count": open_problems_thirty_days_count,
                "chart_open_prb_priority_count": chart_open_prb_priority_count,
                "chart_fix_in_prb_priority_count": chart_fix_in_prb_priority_count,
                "chart_closed_prb_priority_count": chart_closed_prb_priority_count,
                "chart_unassigned_prb_priority_count": chart_unassigned_prb_priority_count,
                "prb_priority_groups": prb_priority_groups,
                "prb_category_open_values": prb_category_open_values,
                "prb_category_fix_in_progress_values": prb_category_fix_in_progress_values,
                "prb_category_closed_values": prb_category_closed_values,
                "prb_category_unassigned_values": prb_category_unassigned_values,
                "prb_category_values": prb_category_values,
                "date_seven_days": date_seven_days,
                "date_thirty_days": date_thirty_days,
                "current_date": current_date,
                "prb_month_enums": prb_month_data,
                "year_data": years,
                "info_title": info_title,
                "from_date": from_date,
                "middle_symbol": middle_symbol,
                "to_date": to_date,
                "param": param,
                "refresh_url": current_path,
            }
        )
        if success:
            return render(request, self.template_name, context=context)

        return HttpResponseBadRequest()


class AjaxProblemsDataTableView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        parsed_query = get_django_datatable_query(raw_request=request.build_absolute_uri())
        success, problems_mgt_list = apis.get_problem_mgt_list_view(request, parsed_query)
        if success:
            self.additional_template_problem_data(problems_mgt_list)
            return JsonResponse(problems_mgt_list.convert_to_dt_response_dict())

        return HttpResponseBadRequest()

    def additional_template_problem_data(self, dt_response: DjangoDTResponse):
        pass  # pass


class AjaxChangeDataTableView(NTTDefaultLoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        parsed_query = get_django_datatable_query(raw_request=request.build_absolute_uri())
        success, change_request_list = apis.get_change_request_list_view(request, parsed_query)
        if success:
            self.additional_template_change_data(change_request_list)
            return JsonResponse(change_request_list.convert_to_dt_response_dict())

        return HttpResponseBadRequest()

    def additional_template_change_data(self, dt_response: DjangoDTResponse):
        pass  # pass


class ChangeRequestView(NTTDefaultLoginRequiredMixin, TemplateView, SegmentBreadCrumbEnabledMixin):
    template_name = "dashboards/change-request.html"

    @property
    def segment(self) -> str:
        return "Change Request Dashboard"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [("Change Request", reverse("dashboards:change-request"))]

    def get(self, request: HttpRequest, *args, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
        }
        current_date = timezone.now().strftime(DATE_TIME_FORMAT)
        current_path = request.path

        param = request.GET.get("param")

        (
            success,
            chg_calculation_response,
        ) = apis.get_change_request_dashboard_calculations(request, GetParamDataDomain(param=param))
        chg_dashboard_values = chg_calculation_response.data

        total_change_count = chg_dashboard_values.get("total_change_count")
        open_change_count = chg_dashboard_values.get("open_change_count")
        assess_change_count = chg_dashboard_values.get("assess_change_count")
        authorize_change_count = chg_dashboard_values.get("authorize_change_count")
        scheduled_change_count = chg_dashboard_values.get("scheduled_change_count")
        implement_change_count = chg_dashboard_values.get("implement_change_count")
        review_change_count = chg_dashboard_values.get("review_change_count")
        closed_change_count = chg_dashboard_values.get("closed_change_count")
        canceled_change_count = chg_dashboard_values.get("canceled_change_count")
        unassigned_change_count = chg_dashboard_values.get("unassigned_change_count")
        chg_not_updated_seven_days_count = chg_dashboard_values.get("chg_not_updated_seven_days_count")
        open_change_thirty_days_count = chg_dashboard_values.get("open_change_thirty_days_count")
        date_seven_days = chg_dashboard_values.get("date_seven_days")
        date_thirty_days = chg_dashboard_values.get("date_thirty_days")
        prb_priority_data = chg_dashboard_values.get("chg_priority_graph_results")
        prb_category_data = chg_dashboard_values.get("chg_category_chart_results")
        chg_years_data = chg_dashboard_values.get("years_data")
        info_title = chg_dashboard_values.get("info_title")
        from_date = chg_dashboard_values.get("from_date")
        middle_symbol = chg_dashboard_values.get("middle_symbol")
        to_date = chg_dashboard_values.get("to_date")
        open_chg_priority_values = []
        scheduled_chg_priority_values = []
        closed_chg_priority_values = []
        unassigned_chg_priority_values = []
        for value in prb_priority_data:
            open_chg_priority_data = value["open_chg_priority_count"]
            open_chg_priority_values.append(open_chg_priority_data)
            scheduled_chg_priority_data = value["scheduled_priority_count"]
            scheduled_chg_priority_values.append(scheduled_chg_priority_data)
            closed_chg_priority_data = value["closed_priority_count"]
            closed_chg_priority_values.append(closed_chg_priority_data)
            unassigned_chg_priority_data = value["unassigned_priority_count"]
            unassigned_chg_priority_values.append(unassigned_chg_priority_data)

        chart_open_chg_priority_count = open_chg_priority_values
        chart_scheduled_chg_priority_count = scheduled_chg_priority_values
        chart_closed_chg_priority_count = closed_chg_priority_values
        chart_unassigned_chg_priority_count = unassigned_chg_priority_values

        chg_priority_groups_data = []
        for group in enums.PriorityGroupsEnum:
            groups_value = group.value[1]
            chg_priority_groups_data.append(groups_value)

        chg_category_open_values = []
        chg_category_scheduled_values = []
        chg_category_closed_values = []
        chg_category_unassigned_values = []
        chg_category_values = []
        for categories in prb_category_data:
            open_chg_category_data = categories["open_chg_category_count"]
            chg_category_open_values.append(open_chg_category_data)
            chg_scheduled_category_data = categories["scheduled_chg_category_count"]
            chg_category_scheduled_values.append(chg_scheduled_category_data)
            closed_chg_category_data = categories["closed_change_category_count"]
            chg_category_closed_values.append(closed_chg_category_data)
            unassigned_chg_category_data = categories["unassigned_change_category_count"]
            chg_category_unassigned_values.append(unassigned_chg_category_data)
            chg_category_list_data = "Null" if categories["category"] is None else categories["category"]
            chg_category_values.append(chg_category_list_data)

        chg_month_data = []
        for month in enums.MonthlyEnum:
            value = month.value
            chg_month_data.append(value)

        years = []
        for value in chg_years_data:
            years_data = value["sla_due_date"]
            years.append(years_data)

        chg_priority_groups = chg_priority_groups_data

        context.update(
            {
                "total_change_count": total_change_count,
                "open_change_count": open_change_count,
                "assess_change_count": assess_change_count,
                "authorize_change_count": authorize_change_count,
                "scheduled_change_count": scheduled_change_count,
                "implement_change_count": implement_change_count,
                "review_change_count": review_change_count,
                "closed_change_count": closed_change_count,
                "canceled_change_count": canceled_change_count,
                "unassigned_change_count": unassigned_change_count,
                "chg_not_updated_seven_days_count": chg_not_updated_seven_days_count,
                "open_change_thirty_days_count": open_change_thirty_days_count,
                "chart_open_chg_priority_count": chart_open_chg_priority_count,
                "chart_scheduled_chg_priority_count": chart_scheduled_chg_priority_count,
                "chart_closed_chg_priority_count": chart_closed_chg_priority_count,
                "chart_unassigned_chg_priority_count": chart_unassigned_chg_priority_count,
                "chg_priority_groups": chg_priority_groups,
                "chg_category_open_values": chg_category_open_values,
                "chg_category_scheduled_values": chg_category_scheduled_values,
                "chg_category_closed_values": chg_category_closed_values,
                "chg_category_unassigned_values": chg_category_unassigned_values,
                "chg_category_values": chg_category_values,
                "date_seven_days": date_seven_days,
                "date_thirty_days": date_thirty_days,
                "current_date": current_date,
                "chg_month_enums": chg_month_data,
                "year_data": years,
                "info_title": info_title,
                "from_date": from_date,
                "middle_symbol": middle_symbol,
                "to_date": to_date,
                "param": param,
                "refresh_url": current_path,
            }
        )
        if success:
            return render(request, self.template_name, context=context)

        return HttpResponseBadRequest()
