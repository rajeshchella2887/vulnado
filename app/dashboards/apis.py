from urllib.parse import urlencode

from datatable_ajax_request_parser.django_extension import DjangoDTRequest, DjangoDTResponse
from django.http import HttpRequest
from ntt_portal_library.contracts.api_contracts.accounts.get_user_contract import (
    GetUserDataDomain,
    GetUserResponseDataDomain,
    get_user__api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.get_users_contract import (
    GetUsersDataDomain,
    GetUsersResponseDataDomain,
    GetUsersResponses,
    GetUsersRestDataDomain,
    get_users_api_path,
)
from ntt_portal_library.domains.common import GenericFailureResponse
from ntt_portal_library.helpers.simple_jwt import build_url_headers_with_jwt_access_token
from utils.api_gateway import api_gateway

GetUserResponses = GetUserResponseDataDomain | GenericFailureResponse


def get_users(
    request: HttpRequest, parsed_query: GetUsersDataDomain | DjangoDTRequest
) -> tuple[bool, GetUsersResponses]:
    ordering = parsed_query.get_order_by()

    params = GetUsersRestDataDomain(
        page=parsed_query.get_page_number(),
        page_size=parsed_query.get_page_size(),
        ordering=ordering[0] if len(ordering) >= 0 else None,
        search=parsed_query.search_value,
    )
    query_params = urlencode(params.to_dict())

    response = api_gateway.get(
        get_users_api_path.get_path(),
        params=query_params,
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    if response.ok:
        response_json_data = GetUsersResponseDataDomain(**response.json()).data
        return response.ok, DjangoDTResponse(
            data=response_json_data.results,
            records_total=response_json_data.count,
            records_filtered=response_json_data.count,
            draw=parsed_query.draw,
            error="",
        )

    return response.ok, GenericFailureResponse(**response.json())


def get_user(request: HttpRequest, data: GetUserDataDomain) -> tuple[bool, GetUserResponses]:
    response = api_gateway.get(
        get_user__api_path.get_path(str(data.username)),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    json_response = response.json()

    if response.ok:
        return response.ok, GetUserResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)
