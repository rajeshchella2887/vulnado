from typing import List, Tuple

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from ntt_portal_library.contracts.api_contracts.providers.add_provider_contract import AddProviderDataDomain
from ntt_portal_library.contracts.api_contracts.providers.delete_provider_contract import DeleteProviderDataDomain
from ntt_portal_library.contracts.api_contracts.providers.get_provider_contract import GetProviderDataDomain
from ntt_portal_library.contracts.api_contracts.providers.update_provider_contract import UpdateProviderDataDomain
from providers.apis import add_provider, delete_provider, get_provider, update_provider
from providers.forms import AddProviderForm, UpdateProviderForm
from utils.mixins.view_mixins import NTTDefaultLoginRequiredMixin, SegmentBreadCrumbEnabledMixin


class AddProviderView(NTTDefaultLoginRequiredMixin, View, SegmentBreadCrumbEnabledMixin):
    form_class = AddProviderForm
    template_name = "providers/add_update_provider.html"

    @property
    def segment(self) -> str:
        return "Add Provider"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [("providers", reverse("dashboards:providers")), ("add provider", reverse("providers:add-provider"))]

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, self.get_context_data(form=form))

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            return self.handle_form_valid(request, form)

        return render(request, self.template_name, self.get_context_data(form=form))

    def handle_form_valid(self, request, form):
        success, response = add_provider(request, AddProviderDataDomain(**form.cleaned_data))

        if success:
            return redirect(reverse("dashboards:providers"))
        else:
            return render(request, self.template_name, self.get_context_data(form=form, errors=response.errors))


class UpdateProviderView(NTTDefaultLoginRequiredMixin, View, SegmentBreadCrumbEnabledMixin):
    form_class = UpdateProviderForm
    template_name = "providers/add_update_provider.html"

    provider_pk: str = None

    @property
    def segment(self) -> str:
        return "Add Provider"

    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        return [
            ("providers", reverse("dashboards:providers")),
            ("update provider", reverse("providers:update-provider", kwargs={"pk": self.provider_pk})),
        ]

    def get(self, request, pk):
        # NOTE: used for path_to_current_view to pass pk to the frontend
        self.provider_pk = pk

        success, response = get_provider(request, GetProviderDataDomain(id=int(self.provider_pk)))
        if success:
            form = self.form_class(initial=response.data.to_dict())
            return render(request, self.template_name, self.get_context_data(form=form))
        else:
            return redirect(reverse("dashboards:providers"))

    def post(self, request, pk):
        self.provider_pk = pk

        form = self.form_class(data=request.POST, initial={"id": pk})
        if form.is_valid():
            return self.handle_form_valid(request, form)

        return render(request, self.template_name, self.get_context_data(form=form))

    def handle_form_valid(self, request, form):
        success, response = update_provider(request, UpdateProviderDataDomain(**form.cleaned_data))
        if success:
            return redirect(reverse("dashboards:providers"))
        else:
            return render(request, self.template_name, self.get_context_data(form=form, errors=response.errors))


class DeleteProviderView(NTTDefaultLoginRequiredMixin, View):
    def delete(self, request, pk):
        success, response = delete_provider(request, DeleteProviderDataDomain(id=pk))

        if success:
            return HttpResponse(f"Provider {pk} deleted")

        return HttpResponseBadRequest()
