from django.urls import path

from . import views, views_ajax

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("settings/ldap/", views.LDAPSettings.as_view(), name="ldap_settings"),
    path("settings/ldap/add/", views.AddLDAPSettingsView.as_view(), name="add_ldap_settings"),
    path("settings/ldap/update/<int:pk>/", views.UpdateLDAPSettingsView.as_view(), name="update_ldap_settings"),
    path("settings/ldap/delete/<int:pk>/", views.DeleteLDAPSettingsView.as_view(), name="delete_ldap_settings"),
    path("ajax-ldap-settings/", views_ajax.AjaxGetLDAPSettingsView.as_view(), name="ajax_ldap_settings"),
    path("create-user/", views.UserOnboardingView.as_view(), name="create_user"),
    path("update-user/<int:user_id>/", views.UserUpdateView.as_view(), name="update_user"),
    path("delete/<int:pk>/", views.DeleteUserView.as_view(), name="delete-user"),
    path("profile-update/", views.LocalUserProfileUpdateView.as_view(), name="profile_update"),
    path("delete-multiple/", views.DeleteMultipleUserView.as_view(), name="delete-multiple-users"),
]
