import json

SERVER_URI_HELP_TEXT = (
    "URI to connect to LDAP server, "
    'such as "ldap://ldap.example.com:389" (non-SSL) or '
    '"ldaps://ldap.example.com:636" (SSL). Multiple LDAP servers '
    "may be specified by separating with spaces or commas. "
    "LDAP authentication is disabled if this parameter is empty."
)
BIND_DN_HELP_TEXT = (
    "DN (Distinguished Name) of user to bind for all search queries. "
    "This is the system user account we will use to login to query LDAP "
    "for other user information. Refer to the documentation for example syntax."
)
BIND_PASSWORD_HELP_TEXT = "Password used to bind LDAP user account."
START_TLS_HELP_TEXT = "Whether to enable TLS when the LDAP connection is not using SSL."
CONNECTION_OPTIONS_HELP_TEXT = (
    "A dictionary of options to pass to each connection to the LDAP server via"
    " LDAPObject.set_option(). Keys are ldap.OPT_* constants."
)
USER_SEARCH_HELP_TEXT = (
    "LDAP search query to find users. Any user that matches the given pattern will be able to "
    "login to the service. The user should also be mapped into an organization (as defined in "
    "the AUTH_LDAP_ORGANIZATION_MAP setting). If multiple search queries need to be supported use "
    'of "LDAPUnion" is possible. See the documentation for details. '
)
USER_DN_TEMPLATE_HELP_TEXT = (
    "Alternative to user search, if user DNs are all of the same format."
    " This approach is more efficient for user lookups than searching "
    "if it is usable in your organizational environment. "
    "If this setting has a value it will be used instead of AUTH_LDAP_USER_SEARCH."
)
USER_ATTR_MAP_HELP_TEXT = (
    "Mapping of LDAP user schema to API user attributes. The default setting is valid for "
    "ActiveDirectory but users with other LDAP configurations may need to change the values. "
    "Refer to the documentation for additional details."
)
GROUP_SEARCH_HELP_TEXT = (
    "Users are mapped to organizations based on their membership in LDAP groups. "
    "This setting defines the LDAP search query to find groups. "
    "Unlike the user search, group search does not support LDAPSearchUnion."
)
GROUP_TYPE_HELP_TEXT = (
    "The group type may need to be changed based on the type of the LDAP server."
    " Values are listed at: "
    "https://django-auth-ldap.readthedocs.io/en/stable/groups.html#types-of-groups"
)
GROUP_TYPE_PARAMS_HELP_TEXT = "Key value parameters to send the chosen group type init method."
REQUIRE_GROUP_HELP_TEXT = (
    "Group DN required to login. If specified, user must be a member of this group to login via "
    "LDAP. If not set, everyone in LDAP that matches the user search will be able to "
    "login to the service. Only one require group is supported."
)
DENY_GROUP_HELP_TEXT = (
    "Group DN denied from login. If specified, user will not be allowed to login "
    "if a member of this group. Only one deny group is supported."
)
# TODO: will need to map this to NTT's own user roles
USER_FLAGS_BY_GROUP_HELP_TEXT = "Retrieve users from a given group. Refer to the documentation for more detail."
ORGANIZATION_MAP_HELP_TEXT = "Maps user DNs to ntt roles. Refer to the documentation for more detail."

NESTED_LDAP_FIELDS = [
    "server_uri",
    "bind_dn",
    "bind_password",
    "start_tls",
    "connection_options",
    "user_search",
    "user_dn_template",
    "user_attr_map",
    # NOTE: we are not supporting multiple group search for now
    "group_search",
    "group_type",
    "group_type_params",
    "require_group",
    "deny_group",
    "user_flags_by_group",
    "organization_map",
]


INITIAL_ORGANIZATION_MAP_JSON_TEMPLATE = {
    "remove": False,
    "organization_user": [
        "cn=engineering,ou=groups,dc=example,dc=com",
        "cn=sales,ou=groups,dc=example,dc=com",
        "cn=it,ou=groups,dc=example,dc=com",
    ],
    "organization_admin": "cn=engineering_admins,ou=groups,dc=example,dc=com",
    "organization_auditor": ["cn=auditor,ou=groups,dc=example,dc=com"],
    "remove_organization_user": True,
    "remove_organization_admin": True,
    "remove_organization_auditor": True,
}
