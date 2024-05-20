import json
from dataclasses import dataclass

from django.http import HttpRequest
from ntt_portal_library.contracts.api_contracts.forms.get_catalog_details_contract import (
    GetCatalogDetailsDataDomain,
    GetCatalogDetailsResponseDataDomain,
    get_catalog_details_api_path,
)
from ntt_portal_library.contracts.api_contracts.forms.get_os_type_contract import (
    GetOSTypeResponseDataDomain,
    get_os_type_api_path,
)
from ntt_portal_library.contracts.api_contracts.forms.post_os_self_query_contract import (
    PostOSSelfQueryDataDomain,
    PostOSSelfQueryResponseDataDomain,
    post_os_self_query_api_path,
)
from ntt_portal_library.contracts.api_contracts.jobs.get_job_contract import (
    GetJobDataDomain,
    GetTemplateResponseDataDomain,
    get_launchjob_api_path,
)
from ntt_portal_library.contracts.api_contracts.jobs.get_job_output_contract import (
    GetJobOutputDataDomain,
    GetJobOutputResponseDataDomain,
    get_job_output_api_path,
)
from ntt_portal_library.contracts.api_contracts.jobs.get_job_status_contract import (
    GetJobStatusDataDomain,
    GetJobStatusResponseDataDomain,
    get_ansible_job_status_api_path,
)
from ntt_portal_library.contracts.api_contracts.jobs.get_jobs_list_contract import (
    GetJobsListDataDomain,
    GetJobsListResponseDataDomain,
    get_jobs_list_api_path,
)
from ntt_portal_library.contracts.api_contracts.jobs.get_provider_type_contract import (
    GetProviderDataDomain,
    GetProviderResponseDataDomain,
    get_provider_type_api_path,
)
from ntt_portal_library.contracts.api_contracts.jobs.post_jobs_contract import (
    PostJobDataDomain,
    PostJobResponseDataDomain,
    launch_job_response_api_path,
)
from ntt_portal_library.contracts.api_contracts.services.get_catalogs_contract import (
    GetCatalogsDataDomain,
    GetCatalogsResponseDataDomain,
    get_catalogs_api_path,
)
from ntt_portal_library.contracts.api_contracts.services.get_credentials_contract import (
    GetCredentialsResponseDataDomain,
    get_credentials_api_path,
)
from ntt_portal_library.contracts.api_contracts.services.get_inventories_contract import (
    GetInventoriesResponseDataDomain,
    get_inventories_api_path,
)
from ntt_portal_library.domains.common import GenericFailureResponse
from ntt_portal_library.helpers.simple_jwt import build_url_headers_with_jwt_access_token
from utils.api_gateway import api_gateway

GetCatalogsResponses = GetCatalogsResponseDataDomain | GenericFailureResponse
GetJobResponses = GetTemplateResponseDataDomain | GenericFailureResponse
GetInventoriesResponses = GetInventoriesResponseDataDomain | GenericFailureResponse
GetCredentialsResponses = GetCredentialsResponseDataDomain | GenericFailureResponse
GetLaunchAnsibleJobResponses = PostJobResponseDataDomain | GenericFailureResponse
GetJobStdoutResponses = GetJobOutputResponseDataDomain | GenericFailureResponse
GetJobsListResponses = GetJobsListResponseDataDomain | GenericFailureResponse
GetProviderTypeResponses = GetProviderResponseDataDomain | GenericFailureResponse

GetAnsibleJobStatusResponses = GetJobStatusResponseDataDomain | GenericFailureResponse
GetOSTypeResponses = GetOSTypeResponseDataDomain | GenericFailureResponse
GetOSSelfQueryResponses = PostOSSelfQueryResponseDataDomain | GenericFailureResponse
GetCatalogDetailsResponses = GetCatalogDetailsResponseDataDomain | GenericFailureResponse


def get_catalogs(request: HttpRequest, data: GetCatalogsDataDomain) -> tuple[bool, GetCatalogsResponses]:
    try:
        response = api_gateway.get(
            get_catalogs_api_path.get_path_with_prefix(str(data.provider)),
            params=data.to_dict(),
            headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        )

        json_response = response.json()

        if response.ok:
            return response.ok, GetCatalogsResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_ansible_job(request: HttpRequest, data: GetJobDataDomain) -> tuple[bool, GetJobResponses]:
    try:
        response = api_gateway.get(
            get_launchjob_api_path.get_path_with_prefix(str(data.template_id)),
            headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        )

        json_response = response.json()

        if response.ok:
            return response.ok, GetTemplateResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_jobs_list(request: HttpRequest, data: GetJobsListDataDomain) -> tuple[bool, GetJobsListResponses]:
    try:
        response = api_gateway.get(
            get_jobs_list_api_path.get_path_with_prefix(),
            params=data.to_dict(),
            headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        )

        json_response = response.json()

        if response.ok:
            return response.ok, GetJobsListResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_inventories_list(request) -> tuple[bool, GetInventoriesResponses]:
    try:
        response = api_gateway.get(
            get_inventories_api_path.get_path_with_prefix(),
            headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        )

        json_response = response.json()

        if response.ok:
            return response.ok, GetInventoriesResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_credentials_list(request) -> tuple[bool, GetCredentialsResponses]:
    try:
        response = api_gateway.get(
            get_credentials_api_path.get_path_with_prefix(),
            headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        )

        json_response = response.json()

        if response.ok:
            return response.ok, GetCredentialsResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_os_type_output(request) -> tuple[bool, GetOSTypeResponses]:
    try:
        response = api_gateway.get(
            get_os_type_api_path.get_path_with_prefix(),
            headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        )
        json_response = response.json()

        if response.ok:
            return response.ok, GetOSTypeResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_catalog_details_output(request, data: GetCatalogDetailsDataDomain) -> tuple[bool, GetCatalogDetailsResponses]:
    try:
        response = api_gateway.get(
            get_catalog_details_api_path.get_path_with_prefix(str(data.catalog_name)),
            params=data.to_dict(),
            headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        )
        json_response = response.json()

        if response.ok:
            return response.ok, GetCatalogDetailsResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_launch_job_response(request: HttpRequest, data: PostJobDataDomain) -> tuple[bool, GetLaunchAnsibleJobResponses]:
    try:
        headers = build_url_headers_with_jwt_access_token(request.session.get("access"))
        headers["Content-Type"] = "application/json"
        json_data = json.dumps(data.to_dict())
        response = api_gateway.post(
            launch_job_response_api_path.get_path_with_prefix(str(data.template_id)),
            data=json_data,
            headers=headers,
        )
        json_response = response.json()
        if response.ok:
            return response.ok, PostJobResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_provider_type(request: HttpRequest, data: GetProviderDataDomain) -> tuple[bool, GetProviderTypeResponses]:
    try:
        response = api_gateway.post(
            get_provider_type_api_path.get_path_with_prefix(),
            data=data.to_dict(),
            headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        )

        json_response = response.json()
        if response.ok:
            return response.ok, GetProviderResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_launch_job_output(request: HttpRequest, data: GetJobOutputDataDomain) -> tuple[bool, GetJobStdoutResponses]:
    try:
        response = api_gateway.post(
            get_job_output_api_path.get_path_with_prefix(),
            data=data.to_dict(),
            headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        )

        json_response = response.json()
        if response.ok:
            return response.ok, GetJobOutputResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_launch_ansible_job_status(
    request: HttpRequest, data: GetJobStatusDataDomain
) -> tuple[bool, GetAnsibleJobStatusResponses]:
    try:
        response = api_gateway.post(
            get_ansible_job_status_api_path.get_path_with_prefix(),
            data=data.to_dict(),
            headers=build_url_headers_with_jwt_access_token(request.session.get("access")),
        )

        json_response = response.json()

        if response.ok:
            return response.ok, GetJobStatusResponseDataDomain(**json_response)

        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()


def get_os_self_query_output(
    request: HttpRequest, data: PostOSSelfQueryDataDomain
) -> tuple[bool, GetOSSelfQueryResponses]:
    try:
        response = api_gateway.post(
            post_os_self_query_api_path.get_path_with_prefix(),
            data=json.dumps(data.to_dict()),
            headers={
                **build_url_headers_with_jwt_access_token(request.session.get("access")),
                "Content-Type": "application/json",
            },
        )
        json_response = response.json()

        if response.ok:
            return response.ok, PostOSSelfQueryResponseDataDomain(**json_response)
        return response.ok, GenericFailureResponse(**json_response)
    except ():
        return False, GenericFailureResponse()
