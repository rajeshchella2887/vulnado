from django.urls import path

from . import views, views_react

app_name = "services"

urlpatterns = [
    path("<str:provider_name>/catalogs/", views.GetCatalogsView.as_view(), name="catalogs"),
    path(
        "<str:provider_name>/catalogs/launchjob/<int:pk>/",
        views.LaunchAnsibleJobView.as_view(),
        name="launch_job",
    ),
    path("jobslist/", views.JobsListView.as_view(), name="jobs_list"),
    path("jobdetails/", views.JobDetailsView.as_view(), name="jobdetails"),
    path("form/", views.FormView.as_view(), name="form"),
    path("remediation/configplan/", views.ConfigPlanView.as_view(), name="configplan"),
]

ajax_paths = [
    path("ajax/launchjob/logs/", views.GetAnsibleJobOutputView.as_view(), name="stdout"),
    path("ajax/launchjob/status/", views.GetAnsibleJobStatusView.as_view(), name="job_status"),
]

react_paths = [
    path("jobs-list/", views_react.ReactGetJobsListView.as_view(), name="get_job_list"),
    path("job-details/", views_react.ReactGetJobOutputView.as_view(), name="get_job_details"),
    path("form/os_type/", views_react.ReactOSTypeView.as_view(), name="get_os_type"),
    path("form/os_self_query/", views_react.ReactOSSelfQueryView.as_view(), name="post_os_self_query"),
    path("form/launch_job/", views_react.ReactJobLaunchView.as_view(), name="form_launch_job"),
    path("form/catalog_details/", views_react.ReactCatalogDetailsView.as_view(), name="form_catalog_details"),
    path("provider_type/", views_react.ReactProviderTypeView.as_view(), name="provider_type"),
]

urlpatterns += ajax_paths
urlpatterns += react_paths
