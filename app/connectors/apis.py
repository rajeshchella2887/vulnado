from urllib.parse import urlencode

from datatable_ajax_request_parser.django_extension import DjangoDTRequest, DjangoDTResponse
from django.http import HttpRequest
from ntt_portal_library.contracts.api_contracts.connectors.get_connectors_contract import (
    GetConnectorDataDomain,
    GetConnectorParamDataDomain,
    GetConnectorResponseDataDomain,
    GetConnectorRestDataDomain,
    get_change_request_list_api_path,
    get_connector_api_path,
    get_connector_dashboard_path,
    get_incidents_sla_api_path,
    get_itsm_proviers_list_api_path,
    get_problems_list_api_path,
)
from ntt_portal_library.contracts.api_contracts.connectors.get_itsm_provider_contract import (
    GetItsmResponseDataDomain,
    GetParamDataDomain,
    get_change_request_calculation_api_path,
    get_incidents_priority_api_path,
    get_itsm_calculation_api_path,
    get_itsm_graph_api_path,
    get_problem_mgt_calculation_api_path,
)
from ntt_portal_library.domains.common import GenericFailureResponse
from ntt_portal_library.helpers.simple_jwt import build_url_headers_with_jwt_access_token
from utils.api_gateway import api_gateway

GetConnectorResponse = DjangoDTResponse | GenericFailureResponse
GetIncidentsResponses = GetConnectorResponseDataDomain | GenericFailureResponse
GetIncidentsCalculationsResponses = GetItsmResponseDataDomain | GenericFailureResponse


def get_incidents(request: HttpRequest) -> tuple[bool, GetIncidentsResponses]:
    response = api_gateway.get(
        get_connector_api_path.get_path_with_prefix(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    json_response = response.json()
    if response.ok:
        return response.ok, GetConnectorResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**response.json())


def get_problem_mgt_list_view(
    request: HttpRequest, parsed_query: GetConnectorDataDomain | DjangoDTRequest
) -> tuple[bool, GetConnectorResponse]:
    ordering = parsed_query.get_order_by()
    state_value = request.GET.get("state")
    day_value = request.GET.get("day")
    month_value = request.GET.get("month")
    year_value = request.GET.get("year")
    filter_value = request.GET.get("filter_param")

    params = GetConnectorParamDataDomain(
        page=parsed_query.get_page_number(),
        page_size=parsed_query.get_page_size(),
        ordering=ordering[0] if len(ordering) > 0 else None,
        search=parsed_query.search_value,
        state=state_value,
        day=day_value,
        month=month_value,
        year=year_value,
        filter_param=filter_value,
    )
    query_params = urlencode(params.to_dict())
    response = api_gateway.get(
        get_problems_list_api_path.get_path_with_prefix(),
        params=query_params,
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    if response.ok:
        response_json_data = GetConnectorResponseDataDomain(**response.json()).data
        return response.ok, DjangoDTResponse(
            data=response_json_data.get("results"),
            records_total=response_json_data.get("count"),
            records_filtered=response_json_data.get("count"),
            draw=parsed_query.draw,
            error="",
        )

    return response.ok, GenericFailureResponse(**response.json())


def get_change_request_list_view(
    request: HttpRequest, parsed_query: GetConnectorDataDomain | DjangoDTRequest
) -> tuple[bool, GetConnectorResponse]:
    ordering = parsed_query.get_order_by()
    state_value = request.GET.get("state")
    day_value = request.GET.get("day")
    month_value = request.GET.get("month")
    year_value = request.GET.get("year")
    filter_value = request.GET.get("filter_param")

    params = GetConnectorParamDataDomain(
        page=parsed_query.get_page_number(),
        page_size=parsed_query.get_page_size(),
        ordering=ordering[0] if len(ordering) > 0 else None,
        search=parsed_query.search_value,
        state=state_value,
        day=day_value,
        month=month_value,
        year=year_value,
        filter_param=filter_value,
    )
    query_params = urlencode(params.to_dict())
    response = api_gateway.get(
        get_change_request_list_api_path.get_path_with_prefix(),
        params=query_params,
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    if response.ok:
        response_json_data = GetConnectorResponseDataDomain(**response.json()).data
        return response.ok, DjangoDTResponse(
            data=response_json_data.get("results"),
            records_total=response_json_data.get("count"),
            records_filtered=response_json_data.get("count"),
            draw=parsed_query.draw,
            error="",
        )

    return response.ok, GenericFailureResponse(**response.json())


def get_incidents_dashboard_view(
    request: HttpRequest, parsed_query: GetConnectorDataDomain | DjangoDTRequest
) -> tuple[bool, GetConnectorResponse]:
    ordering = parsed_query.get_order_by()
    state_value = request.GET.get("state")
    day_value = request.GET.get("day")
    month_value = request.GET.get("month")
    year_value = request.GET.get("year")
    filter_value = request.GET.get("filter_param")

    params = GetConnectorParamDataDomain(
        page=parsed_query.get_page_number(),
        page_size=parsed_query.get_page_size(),
        ordering=ordering[0] if len(ordering) > 0 else None,
        search=parsed_query.search_value,
        state=state_value,
        day=day_value,
        month=month_value,
        year=year_value,
        filter_param=filter_value,
    )
    query_params = urlencode(params.to_dict())
    response = api_gateway.get(
        get_connector_dashboard_path.get_path_with_prefix(),
        params=query_params,
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    if response.ok:
        response_json_data = GetConnectorResponseDataDomain(**response.json()).data
        return response.ok, DjangoDTResponse(
            data=response_json_data.get("results"),
            records_total=response_json_data.get("count"),
            records_filtered=response_json_data.get("count"),
            draw=parsed_query.draw,
            error="",
        )

    return response.ok, GenericFailureResponse(**response.json())


def get_incidents_list(
    request: HttpRequest, parsed_query: GetConnectorDataDomain | DjangoDTRequest
) -> tuple[bool, GetConnectorResponse]:
    ordering = parsed_query.get_order_by()
    day_value = request.GET.get("day")
    month_value = request.GET.get("month")
    year_value = request.GET.get("year")

    params = GetConnectorRestDataDomain(
        page=parsed_query.get_page_number(),
        page_size=parsed_query.get_page_size(),
        ordering=ordering[0] if len(ordering) > 0 else None,
        search=parsed_query.search_value,
        day=day_value,
        month=month_value,
        year=year_value,
    )
    query_params = urlencode(params.to_dict())

    response = api_gateway.get(
        get_itsm_proviers_list_api_path.get_path_with_prefix(),
        params=query_params,
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    if response.ok:
        response_json_data = GetConnectorResponseDataDomain(**response.json()).data
        return response.ok, DjangoDTResponse(
            data=response_json_data.get("results"),
            records_total=response_json_data.get("count"),
            records_filtered=response_json_data.get("count"),
            draw=parsed_query.draw,
            error="",
        )

    return response.ok, GenericFailureResponse(**response.json())


def get_itsm_sla(request: HttpRequest) -> tuple[bool, GetIncidentsResponses]:
    sla_response = api_gateway.get(
        get_incidents_sla_api_path.get_path_with_prefix(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    sla_json_response = sla_response.json()
    if sla_response.ok:
        return sla_response.ok, GetConnectorResponseDataDomain(**sla_json_response)

    return sla_response.ok, GenericFailureResponse(**sla_response.json())


def get_itsm_dashboard_calculations(
    request: HttpRequest, param: GetParamDataDomain
) -> tuple[bool, GetIncidentsCalculationsResponses]:
    calculations_response = api_gateway.get(
        get_itsm_calculation_api_path.get_path_with_prefix(),
        params=param.to_dict(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    calculations_json = calculations_response.json()

    if calculations_response.ok:
        return calculations_response.ok, GetItsmResponseDataDomain(**calculations_json)

    return calculations_response.ok, GenericFailureResponse(**calculations_json.json())


def get_problem_mgt_dashboard_calculations(
    request: HttpRequest, param: GetParamDataDomain
) -> tuple[bool, GetIncidentsCalculationsResponses]:
    prb_calculations_response = api_gateway.get(
        get_problem_mgt_calculation_api_path.get_path_with_prefix(),
        params=param.to_dict(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    prb_calculations_json = prb_calculations_response.json()

    if prb_calculations_response.ok:
        return prb_calculations_response.ok, GetItsmResponseDataDomain(**prb_calculations_json)

    return prb_calculations_response.ok, GenericFailureResponse(**prb_calculations_json.json())


def get_change_request_dashboard_calculations(
    request: HttpRequest, param: GetParamDataDomain
) -> tuple[bool, GetIncidentsCalculationsResponses]:
    chg_calculations_response = api_gateway.get(
        get_change_request_calculation_api_path.get_path_with_prefix(),
        params=param.to_dict(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    chg_calculations_json = chg_calculations_response.json()

    if chg_calculations_response.ok:
        return chg_calculations_response.ok, GetItsmResponseDataDomain(**chg_calculations_json)

    return chg_calculations_response.ok, GenericFailureResponse(**chg_calculations_json.json())


def get_itsm_graph_calculations(
    request: HttpRequest,
) -> tuple[bool, GetIncidentsCalculationsResponses]:
    graph_calculations_response = api_gateway.get(
        get_itsm_graph_api_path.get_path_with_prefix(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    graph_json = graph_calculations_response.json()
    if graph_calculations_response.ok:
        return graph_calculations_response.ok, GetItsmResponseDataDomain(**graph_json)

    return graph_calculations_response.ok, GenericFailureResponse(**graph_calculations_response.json())


def get_itsm_priority_chart_calculations(
    request: HttpRequest,
) -> tuple[bool, GetIncidentsCalculationsResponses]:
    priority_calculations_response = api_gateway.get(
        get_incidents_priority_api_path.get_path_with_prefix(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    priority_json = priority_calculations_response.json()
    if priority_calculations_response.ok:
        return priority_calculations_response.ok, GetItsmResponseDataDomain(**priority_json)

    return priority_calculations_response.ok, GenericFailureResponse(**priority_calculations_response.json())
