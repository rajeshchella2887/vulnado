from django.urls import path

from . import views, views_ajax, views_itsm

app_name = "dashboards"

urlpatterns = [
    path("", views.DashboardIndexView.as_view(), name="index"),
    path("providers/", views.ProvidersView.as_view(), name="providers"),
    path("connectors/", views_itsm.ConnectorsView.as_view(), name="connectors"),
    path(
        "problem-management/",
        views_itsm.ProblemMgtView.as_view(),
        name="problem-management",
    ),
    path("change-request/", views_itsm.ChangeRequestView.as_view(), name="change-request"),
    path(
        "compliance-management/",
        views.ComplianceMgtView.as_view(),
        name="compliance-management",
    ),
    path(
        "ajax_providers/",
        views_ajax.AjaxGetProvidersView.as_view(),
        name="ajax_providers",
    ),
    path("authorization/", views.AuthorizationView.as_view(), name="authorization"),
    path("authentication/", views.AuthenticationView.as_view(), name="authentication"),
    path(
        "compliance-management/",
        views.ComplianceMgtView.as_view(),
        name="compliance-management",
    ),
    path("asset-management", views.AssetMgtView.as_view(), name="asset-management"),
    path("tree/", views_ajax.AjaxOrganizationTreeView.as_view(), name="tree"),
    path(
        "users/details/<str:username>/",
        views_ajax.AjaxUserDetailsView.as_view(),
        name="user_details",
    ),
    path(
        "organizations/<str:org_name>/",
        views_ajax.AjaxOrganizationDetailsView.as_view(),
        name="org",
    ),
    path(
        "groups/<str:group_name>/",
        views_ajax.AjaxGroupDetailsView.as_view(),
        name="groups",
    ),
    path(
        "ajax_incidents_graph/",
        views_ajax.AjaxIncidentsSlaGraphView.as_view(),
        name="ajax_incidents_graph",
    ),
    path(
        "ajax_incidents_datatable/",
        views_ajax.AjaxIncidentsDataTableView.as_view(),
        name="ajax_incidents_datatable",
    ),
    path(
        "ajax_problems_datatable/",
        views_itsm.AjaxProblemsDataTableView.as_view(),
        name="ajax_problems_datatable",
    ),
    path(
        "ajax_change_datatable/",
        views_itsm.AjaxChangeDataTableView.as_view(),
        name="ajax_change_datatable",
    ),
    path(
        "incidents_dashboard/",
        views_ajax.AjaxIncidentDashboardView.as_view(),
        name="incidents_dashboard",
    ),
    path("users/", views.UsersView.as_view(), name="users"),
    path("ajax_users/", views_ajax.AjaxGetUsersView.as_view(), name="ajax_users"),
]
