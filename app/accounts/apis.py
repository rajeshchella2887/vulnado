import json
from typing import List
from urllib.parse import urlencode

from datatable_ajax_request_parser.django_extension import DjangoDTRequest, DjangoDTResponse
from django.http import HttpRequest
from ntt_portal_library.contracts.api_contracts.accounts.add_ldap_settings_contract import (
    AddLDAPSettingsDataDomain,
    AddLDAPSettingsResponseDataDomain,
    add_ldap_settings_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.create_ldap_user_contract import (
    CreateLdapUserDataDomain,
    CreateLdapUserResponseDataDomain,
    accounts_create_ldap_user_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.create_user_contract import (
    CreateUserDataDomain,
    CreateUserResponseDataDomain,
    accounts_create_user_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.delete_ldap_settings_contract import (
    DeleteLDAPSettingsDataDomain,
    DeleteLDAPSettingsResponseDataDomain,
    delete_ldap_settings_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.delete_multiple_users_contract import (
    delete_multiple_users_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.delete_user_contract import (
    DeleteUserDataDomain,
    DeleteUserResponseDataDomain,
    delete_user_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.get_ldap_settings_contract import (
    GetLDAPSettingsDataDomain,
    GetLDAPSettingsResponseDataDomain,
    GetLDAPSettingsRestDataDomain,
    get_ldap_settings_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.get_ldap_settings_for_update_contract import (
    GetLDAPSettingsForUpdateDataDomain,
    GetLDAPSettingsForUpdateResponseDataDomain,
    get_ldap_settings_for_update_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.profile_update_contract import (
    user_profile_getorupdate_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.update_ad_user_contract import (
    UpdateAdUserDataDomain,
    UpdateAdUserDataDomainResponseDataDomain,
    accounts_update_ad_user_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.update_user_contract import (
    UpdateUserDataDomain,
    UpdateUserResponseDataDomain,
    accounts_get_user_id_for_update_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.update_user_without_password_contract import (
    UpdateUserWithoutPasswordDataDomain,
    UpdateUserWithoutPasswordResponseDataDomain,
    accounts_get_user_id_for_update_without_password_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.user_login_contract import (
    UserLoginDataDomain,
    UserLoginResponseDataDomain,
    accounts_login_api_path,
)
from ntt_portal_library.contracts.api_contracts.accounts.user_logout_contract import (
    UserLogoutDataDomain,
    UserLogoutResponseDataDomain,
    accounts_logout_api_path,
)
from ntt_portal_library.domains.auth.ldap_settings import LDAPSettings
from ntt_portal_library.domains.common import GenericFailureResponse
from ntt_portal_library.helpers.simple_jwt import build_url_headers_with_jwt_access_token
from utils.api_gateway import api_gateway

UserLoginResponses = UserLoginResponseDataDomain | GenericFailureResponse
LogoutAccountsResponses = UserLogoutResponseDataDomain | GenericFailureResponse
GetLDAPSettingsResponses = DjangoDTResponse | GenericFailureResponse
AddLDAPSettingsResponses = AddLDAPSettingsResponseDataDomain | GenericFailureResponse
GetLDAPSettingsForUpdateResponses = GetLDAPSettingsForUpdateResponseDataDomain | GenericFailureResponse
DeleteLDAPSettingsResponses = DeleteLDAPSettingsResponseDataDomain | GenericFailureResponse
CreateUserResponses = CreateUserResponseDataDomain | GenericFailureResponse
CreateLdapUserResponses = CreateLdapUserResponseDataDomain | GenericFailureResponse
DeleteUserResponses = DeleteUserResponseDataDomain | GenericFailureResponse
DeleteMultiUserResponses = DeleteUserResponseDataDomain | GenericFailureResponse
UpdateUserWithoutPasswordResponses = UpdateUserWithoutPasswordResponseDataDomain | GenericFailureResponse
UpdateAdUserResponses = UpdateAdUserDataDomainResponseDataDomain | GenericFailureResponse


def user_login(data: UserLoginDataDomain) -> tuple[bool, UserLoginResponses]:
    response = api_gateway.post(accounts_login_api_path.get_path(), data=data.to_dict())
    json_response = response.json()
    if response.ok:
        return response.ok, UserLoginResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def user_logout(data: UserLogoutDataDomain) -> tuple[bool, LogoutAccountsResponses]:
    response = api_gateway.post(accounts_logout_api_path.get_path(), data=data.to_dict())
    json_response = response.json()
    if response.ok:
        return response.ok, UserLogoutResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def get_ldap_settings(
    request: HttpRequest, parsed_query: GetLDAPSettingsDataDomain | DjangoDTRequest
) -> tuple[bool, GetLDAPSettingsResponses]:
    ordering = parsed_query.get_order_by()

    params = GetLDAPSettingsRestDataDomain(
        page=parsed_query.get_page_number(),
        page_size=parsed_query.get_page_size(),
        ordering=ordering[0] if len(ordering) >= 0 else None,
        search=parsed_query.search_value,
    )
    query_params = urlencode(params.to_dict())

    response = api_gateway.get(
        get_ldap_settings_api_path.get_path(),
        params=query_params,
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    if response.ok:
        response_json_data = GetLDAPSettingsResponseDataDomain(**response.json()).data
        return response.ok, DjangoDTResponse(
            data=response_json_data.results,
            records_total=response_json_data.count,
            records_filtered=response_json_data.count,
            draw=parsed_query.draw,
            error="",
        )

    return response.ok, GenericFailureResponse(**response.json())


def add_ldap_settings(request: HttpRequest, data: AddLDAPSettingsDataDomain) -> tuple[bool, AddLDAPSettingsResponses]:
    # NOTE: nested data need special handling, hence we need to dump
    headers = {
        **build_url_headers_with_jwt_access_token(request.session.get("access")),
        "Content-Type": "application/json",
    }
    response = api_gateway.post(
        add_ldap_settings_api_path.get_path(),
        data=json.dumps(data.to_dict()),
        headers=headers,
    )

    json_response = response.json()
    if response.ok:
        return response.ok, AddLDAPSettingsResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def get_ldap_settings_for_update(
    request: HttpRequest, data: GetLDAPSettingsForUpdateDataDomain
) -> tuple[bool, GetLDAPSettingsForUpdateResponses]:
    response = api_gateway.get(
        get_ldap_settings_for_update_api_path.get_path(str(data.id)),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    json_response = response.json()

    if response.ok:
        return response.ok, GetLDAPSettingsForUpdateResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def update_ldap_settings(
    request: HttpRequest,
    data: GetLDAPSettingsForUpdateDataDomain,
    payload: LDAPSettings,
) -> tuple[bool, GetLDAPSettingsForUpdateResponses]:
    headers = {
        **build_url_headers_with_jwt_access_token(request.session.get("access")),
        "Content-Type": "application/json",
    }
    response = api_gateway.put(
        get_ldap_settings_for_update_api_path.get_path(str(data.id)),
        data=json.dumps(payload.to_dict()),
        headers=headers,
    )

    json_response = response.json()

    if response.ok:
        return response.ok, GetLDAPSettingsForUpdateResponseDataDomain(**json_response)

    return response.ok, GenericFailureResponse(**json_response)


def delete_ldap_settings(
    request: HttpRequest, data: DeleteLDAPSettingsDataDomain
) -> tuple[bool, DeleteLDAPSettingsResponses]:
    response = api_gateway.delete(
        delete_ldap_settings_api_path.get_path(str(data.id)),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    if response.ok:
        return response.ok, DeleteLDAPSettingsResponseDataDomain(success=response.ok, data=None)

    return response.ok, GenericFailureResponse(**response.json())


# user onboarding
def add_user(request: HttpRequest, data: CreateUserDataDomain) -> tuple[bool, CreateUserResponses]:
    headers = {
        **build_url_headers_with_jwt_access_token(request.session.get("access")),
        "Content-Type": "application/json",
    }
    response = api_gateway.post(
        accounts_create_user_api_path.get_path(),
        data=json.dumps(data.to_dict()),
        headers=headers,
    )

    json_response = response.json()
    if response.ok:
        return response.ok, CreateUserResponseDataDomain(**json_response)

    return response.ok, json_response


def get_user_group(access):
    headers = {
        **build_url_headers_with_jwt_access_token(access),
        "Content-Type": "application/json",
    }
    response = api_gateway.get(
        accounts_create_user_api_path.get_path(),
        headers=headers,
    )
    json_response = response.json()
    if response.ok:
        return response.ok, json_response

    return response.ok, json_response


# create ldap user
def create_ldap_user(request: HttpRequest, data: CreateLdapUserDataDomain) -> tuple[bool, CreateLdapUserResponses]:
    headers = {
        **build_url_headers_with_jwt_access_token(request.session.get("access")),
        "Content-Type": "application/json",
    }
    response = api_gateway.post(
        accounts_create_ldap_user_api_path.get_path(),
        data=json.dumps(data.to_dict()),
        headers=headers,
    )

    json_response = response.json()
    if response.ok:
        return response.ok, json_response

    return response.ok, json_response


# getting user data with id
def get_user_for_update(request: HttpRequest, user_id):
    headers = {
        **build_url_headers_with_jwt_access_token(request.session.get("access")),
        "Content-Type": "application/json",
    }
    response = api_gateway.get(
        accounts_get_user_id_for_update_api_path.get_path(str(user_id)),
        headers=headers,
    )
    json_response = response.json()

    if response.ok:
        return response.ok, json_response

    return response.ok, json_response


# update local user
def update_user(
    request: HttpRequest, data: UpdateUserDataDomain, user_id
) -> tuple[bool, GetLDAPSettingsForUpdateResponses]:
    headers = {
        **build_url_headers_with_jwt_access_token(request.session.get("access")),
        "Content-Type": "application/json",
    }
    response = api_gateway.put(
        accounts_get_user_id_for_update_api_path.get_path(str(user_id)),
        data=json.dumps(data.to_dict()),
        headers=headers,
    )
    json_response = response.json()
    if response.ok:
        return response.ok, UpdateUserResponseDataDomain(**json_response)

    return response.ok, json_response


def update_user_without_password(
    request: HttpRequest, data: UpdateUserWithoutPasswordDataDomain, user_id
) -> tuple[bool, UpdateUserWithoutPasswordResponses]:
    headers = {
        **build_url_headers_with_jwt_access_token(request.session.get("access")),
        "Content-Type": "application/json",
    }
    response = api_gateway.put(
        accounts_get_user_id_for_update_without_password_api_path.get_path(str(user_id)),
        data=json.dumps(data.to_dict()),
        headers=headers,
    )

    json_response = response.json()

    if response.ok:
        return response.ok, UpdateUserWithoutPasswordResponseDataDomain(**json_response)

    return response.ok, json_response


def update_ad_user(request: HttpRequest, data: UpdateAdUserDataDomain) -> tuple[bool, UpdateAdUserResponses]:
    headers = {
        **build_url_headers_with_jwt_access_token(request.session.get("access")),
        "Content-Type": "application/json",
    }
    response = api_gateway.put(
        accounts_update_ad_user_api_path.get_path(str(data.id)),
        data=json.dumps(data.to_dict()),
        headers=headers,
    )

    json_response = response.json()
    if response.ok:
        return response.ok, UpdateAdUserDataDomainResponseDataDomain(**json_response)

    return response.ok, json_response


def delete_user(request: HttpRequest, data: DeleteUserDataDomain) -> tuple[bool, DeleteUserResponses]:
    response = api_gateway.delete(
        delete_user_api_path.get_path(str(data.id)),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )

    if response.ok:
        return response.ok, DeleteUserResponseDataDomain(success=response.ok, data=None)

    return response.ok, GenericFailureResponse(**response.json())


def delete_users(request, user_ids: List[int]) -> tuple[bool, DeleteMultiUserResponses]:
    response = api_gateway.delete(
        delete_multiple_users_api_path.get_path(),
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        json={"id": user_ids},
    )

    if response.ok:
        return response.ok, DeleteUserResponseDataDomain(success=response.ok, data=None)

    return response.ok, GenericFailureResponse(**response.json())


def getting_user_profile(request: HttpRequest, username):
    headers = {
        **build_url_headers_with_jwt_access_token(request.session.get("access")),
        "Content-Type": "application/json",
    }
    response = api_gateway.get(
        user_profile_getorupdate_api_path.get_path(str(username)),
        headers=headers,
    )
    json_response = response.json()
    if response.ok:
        return response.ok, json_response

    return response.ok, json_response


def updating_user_profile(request: HttpRequest, data, username, files):
    response = api_gateway.put(
        user_profile_getorupdate_api_path.get_path(str(username)),
        data=data.to_dict(),
        files=files,
        headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
    )
    json_response = response.json()
    if response.ok:
        return response.ok, json_response

    return response.ok, json_response
