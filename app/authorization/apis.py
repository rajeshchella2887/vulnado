from django.http import HttpRequest
from ntt_portal_library.contracts.api_contracts.roles.get_group_details_contract import (
    GetGroupDetailsDataDomain,
    GetGroupDetailsResponseDataDomain,
    get_group_details_api_path,
)
from ntt_portal_library.contracts.api_contracts.roles.get_organization_details_contract import (
    GetOrganizationDetailsDataDomain,
    GetOrganizationDetailsResponseDataDomain,
    get_organization_details_api_path,
)
from ntt_portal_library.contracts.api_contracts.roles.get_organizations_tree_contract import (
    GetOrganizationTreeResponseDataDomain,
    get_organizations_tree_api_path,
)
from ntt_portal_library.contracts.api_contracts.roles.get_user_details_contract import (
    GetUserDetailsDataDomain,
    GetUserDetailsResponseDataDomain,
    get_users_details_api_path,
)
from ntt_portal_library.domains.common import GenericFailureResponse
from ntt_portal_library.helpers.simple_jwt import build_url_headers_with_jwt_access_token
from utils.api_gateway import api_gateway

GetOrganizationTreeResponses = GetOrganizationTreeResponseDataDomain | GenericFailureResponse
GetOrganizationDetailsResponses = GetOrganizationDetailsResponseDataDomain | GenericFailureResponse
GetGroupDetailsResponses = GetGroupDetailsResponseDataDomain | GenericFailureResponse
GetUserDetailsResponses = GetUserDetailsResponseDataDomain | GenericFailureResponse


def get_organization_tree(request: HttpRequest) -> tuple[bool, GetOrganizationTreeResponses]:
    response = api_gateway.get(
        get_organizations_tree_api_path.get_path(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    json_response = response.json()

    if response.ok:
        return response.ok, GetOrganizationTreeResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def get_organization_details(
    request: HttpRequest, data: GetOrganizationDetailsDataDomain
) -> tuple[bool, GetOrganizationDetailsResponses]:
    response = api_gateway.get(
        get_organization_details_api_path.get_path(data.name),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    json_response = response.json()

    if response.ok:
        return response.ok, GetOrganizationDetailsResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def get_group_details(request: HttpRequest, data: GetGroupDetailsDataDomain) -> tuple[bool, GetGroupDetailsResponses]:
    response = api_gateway.get(
        get_group_details_api_path.get_path(data.name),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    json_response = response.json()

    if response.ok:
        return response.ok, GetGroupDetailsResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def get_user_details(request: HttpRequest, data: GetUserDetailsDataDomain) -> tuple[bool, GetUserDetailsResponses]:
    response = api_gateway.get(
        get_users_details_api_path.get_path(data.name),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    json_response = response.json()

    if response.ok:
        return response.ok, GetUserDetailsResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)
