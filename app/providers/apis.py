from urllib.parse import urlencode

from datatable_ajax_request_parser.django_extension import DjangoDTRequest, DjangoDTResponse
from django.http import HttpRequest
from ntt_portal_library.contracts.api_contracts.providers.add_provider_contract import (
    AddProviderDataDomain,
    AddProviderResponseDataDomain,
    add_provider_api_path,
)
from ntt_portal_library.contracts.api_contracts.providers.delete_provider_contract import (
    DeleteProviderDataDomain,
    DeleteProviderResponseDataDomain,
    delete_provider_api_path,
)
from ntt_portal_library.contracts.api_contracts.providers.get_provider_contract import (
    GetProviderDataDomain,
    GetProviderResponseDataDomain,
    get_provider_api_path,
)
from ntt_portal_library.contracts.api_contracts.providers.get_providers_contract import (
    GetProvidersDataDomain,
    GetProvidersResponseDataDomain,
    GetProvidersRestDataDomain,
    get_providers_api_path,
)
from ntt_portal_library.contracts.api_contracts.providers.update_provider_contract import (
    UpdateProviderDataDomain,
    UpdateProviderResponseDataDomain,
    update_provider_api_path,
)
from ntt_portal_library.domains.common import GenericFailureResponse
from ntt_portal_library.helpers.simple_jwt import build_url_headers_with_jwt_access_token
from utils.api_gateway import api_gateway

AddProviderResponses = AddProviderResponseDataDomain | GenericFailureResponse
GetProviderResponses = GetProviderResponseDataDomain | GenericFailureResponse
GetProvidersResponses = DjangoDTResponse | GenericFailureResponse
UpdateProviderResponses = UpdateProviderResponseDataDomain | GenericFailureResponse
DeleteProviderResponses = DeleteProviderResponseDataDomain | GenericFailureResponse


def add_provider(request: HttpRequest, data: AddProviderDataDomain) -> tuple[bool, AddProviderResponses]:
    response = api_gateway.post(
        add_provider_api_path.get_path_with_prefix(),
        data=data.to_dict(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    json_response = response.json()
    if response.ok:
        return response.ok, AddProviderResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def get_provider(request: HttpRequest, data: GetProviderDataDomain) -> tuple[bool, GetProviderResponses]:
    response = api_gateway.get(
        get_provider_api_path.get_path_with_prefix(str(data.id)),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    json_response = response.json()
    if response.ok:
        return response.ok, GetProviderResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def get_providers(
    request: HttpRequest, parsed_query: GetProvidersDataDomain | DjangoDTRequest
) -> tuple[bool, GetProvidersResponses]:
    ordering = parsed_query.get_order_by()

    params = GetProvidersRestDataDomain(
        page=parsed_query.get_page_number(),
        page_size=parsed_query.get_page_size(),
        ordering=ordering[0] if len(ordering) >= 0 else None,
        search=parsed_query.search_value,
    )
    query_params = urlencode(params.to_dict())

    response = api_gateway.get(
        get_providers_api_path.get_path_with_prefix(),
        params=query_params,
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    if response.ok:
        response_json_data = GetProvidersResponseDataDomain(**response.json()).data
        return response.ok, DjangoDTResponse(
            data=response_json_data.results,
            records_total=response_json_data.count,
            records_filtered=response_json_data.count,
            draw=parsed_query.draw,
            error="",
        )

    return response.ok, GenericFailureResponse(**response.json())


def update_provider(request: HttpRequest, data: UpdateProviderDataDomain) -> tuple[bool, UpdateProviderResponses]:
    response = api_gateway.put(
        update_provider_api_path.get_path_with_prefix(data.id),
        data=data.to_dict(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    json_response = response.json()
    if response.ok:
        return response.ok, UpdateProviderResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def delete_provider(request: HttpRequest, data: DeleteProviderDataDomain) -> tuple[bool, DeleteProviderResponses]:
    response = api_gateway.delete(
        delete_provider_api_path.get_path_with_prefix(str(data.id)),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    if response.ok:
        return response.ok, DeleteProviderResponseDataDomain(success=response.ok, data=None)

    return response.ok, GenericFailureResponse(**response.json())
