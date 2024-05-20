from enum import Enum

from ntt_portal_library.rbac.local_permission_registry.registry import permission_registry
from ntt_portal_library.rbac.local_permission_registry.role_definition import NTTRoleDefinition
from ntt_portal_library.rbac.roles import NTTPortalRoles


class NTTPortalPagesPermissions(Enum):
    LOGIN_PAGE = "ntt_login"
    DASHBOARD = "ntt_dashboard"
    DASHBOARD_COMPLIANCE = "ntt_dashboard_compliance"
    DASHBOARD_PATCH_MANAGEMENT = "ntt_dashboard_patch_management"
    DASHBOARD_ASSET_MANAGEMENT = "ntt_dashboard_asset_management"
    DASHBOARD_SERVICENOW = "ntt_dashboard_servicenow"
    SERVICE_CATALOGS = "ntt_service_catalogs"
    SERVICE_CATALOGS_PROVIDERS = "ntt_service_catalogs_providers"
    SERVICE_CATALOGS_AUTOMATION_PROVIDERS = "ntt_service_catalogs_automation_providers"
    SERVICE_CATALOGS_ITSM_PROVIDERS = "ntt_service_catalogs_itsm_providers"
    SERVICE_CATALOGS_NETWORK_PROVIDERS = "ntt_service_catalogs_network_providers"
    SERVICE_CATALOGS_COMPLIANCE_MANAGEMENT = "ntt_service_catalogs_compliance_management"
    SERVICE_CATALOGS_AD_HOC_SCANNING = "ntt_service_catalogs_ad_hoc_scanning"
    SERVICE_CATALOGS_CONFIGURATION_PLAN = "ntt_service_catalogs_configuration_plan"
    SERVICE_CATALOGS_PATCH_MANAGEMENT = "ntt_service_catalogs_patch_management"
    SERVICE_CATALOGS_ASSET_MANAGEMENT = "ntt_service_catalogs_asset_management"
    ADMIN = "ntt_admin"
    ADMIN_GROUPS = "ntt_admin_groups"
    ADMIN_USERS = "ntt_admin_users"
    ADMIN_AUTHORIZATION = "ntt_admin_authorization"
    ADMIN_AUTHENTICATION = "ntt_admin_authentication"


@permission_registry.register_role_permission_registry
class OrganizationAdmin(NTTRoleDefinition):
    available_permissions = {
        NTTPortalPagesPermissions.LOGIN_PAGE.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_AUTOMATION_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_ITSM_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_NETWORK_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_COMPLIANCE_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_AD_HOC_SCANNING.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_CONFIGURATION_PLAN.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_PATCH_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_ASSET_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.DASHBOARD.value: True,
        NTTPortalPagesPermissions.DASHBOARD_COMPLIANCE.value: True,
        NTTPortalPagesPermissions.DASHBOARD_ASSET_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.DASHBOARD_PATCH_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.DASHBOARD_SERVICENOW.value: True,
        NTTPortalPagesPermissions.ADMIN.value: True,
        NTTPortalPagesPermissions.ADMIN_USERS.value: True,
        NTTPortalPagesPermissions.ADMIN_GROUPS.value: True,
        NTTPortalPagesPermissions.ADMIN_AUTHENTICATION.value: True,
        NTTPortalPagesPermissions.ADMIN_AUTHORIZATION.value: True,
    }


# NOTE: this is dependent on the organization admin
@permission_registry.register_role_permission_registry
class OrganizationUser(NTTRoleDefinition):
    available_permissions = {
        NTTPortalPagesPermissions.LOGIN_PAGE.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_AUTOMATION_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_ITSM_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_NETWORK_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_COMPLIANCE_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_AD_HOC_SCANNING.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_CONFIGURATION_PLAN.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_PATCH_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_ASSET_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.DASHBOARD.value: True,
        NTTPortalPagesPermissions.DASHBOARD_COMPLIANCE.value: True,
        NTTPortalPagesPermissions.DASHBOARD_ASSET_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.DASHBOARD_PATCH_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.DASHBOARD_SERVICENOW.value: True,
    }


@permission_registry.register_role_permission_registry
class OrganizationAuditor(NTTRoleDefinition):
    available_permissions = {
        NTTPortalPagesPermissions.LOGIN_PAGE.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_AUTOMATION_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_ITSM_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_NETWORK_PROVIDERS.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_COMPLIANCE_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_AD_HOC_SCANNING.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_CONFIGURATION_PLAN.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_PATCH_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.SERVICE_CATALOGS_ASSET_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.DASHBOARD.value: True,
        NTTPortalPagesPermissions.DASHBOARD_COMPLIANCE.value: True,
        NTTPortalPagesPermissions.DASHBOARD_ASSET_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.DASHBOARD_PATCH_MANAGEMENT.value: True,
        NTTPortalPagesPermissions.DASHBOARD_SERVICENOW.value: True,
        NTTPortalPagesPermissions.ADMIN.value: True,
        NTTPortalPagesPermissions.ADMIN_USERS.value: True,
        NTTPortalPagesPermissions.ADMIN_GROUPS.value: True,
        NTTPortalPagesPermissions.ADMIN_AUTHENTICATION.value: True,
        NTTPortalPagesPermissions.ADMIN_AUTHORIZATION.value: True,
    }


def determine_role(user_role):
    if not user_role:
        raise ValueError("no user_role provided")

    if user_role == NTTPortalRoles.ORGANIZATION_ADMIN.value:
        return OrganizationAdmin
    elif user_role == NTTPortalRoles.ORGANIZATION_USER.value:
        return OrganizationUser
    elif user_role == NTTPortalRoles.ORGANIZATION_AUDITOR.value:
        return OrganizationAuditor

    raise ValueError(f"user_role {user_role} is not supported")
