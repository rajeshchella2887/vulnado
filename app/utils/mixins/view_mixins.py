from typing import List, Tuple

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.base import ContextMixin


class SegmentMixin:
    @property
    def segment(self) -> str:
        raise NotImplementedError(f"{self.__class__.__name__}.segment is not implemented")

    def get_segment(self) -> str:
        return self.segment


class BreadCrumbMixin:
    @property
    def path_to_current_view(self) -> List[Tuple[str, str]]:
        raise NotImplementedError(f"{self.__class__.__name__}.path_to_current_view is not implemented")

    def get_breadcrumbs(self, home: Tuple[str, str] = None) -> List[Tuple[str, str]]:
        path = self.path_to_current_view

        home = home if home else reverse("dashboards:index")

        return [("home", home), *path]


class SegmentBreadCrumbEnabledMixin(BreadCrumbMixin, SegmentMixin, ContextMixin):
    def get_context_data(self, **kwargs):
        kwargs.update({"breadcrumbs": self.get_breadcrumbs(), "segment": self.get_segment()})
        return super().get_context_data(**kwargs)


class NTTDefaultLoginRequiredMixin(LoginRequiredMixin):
    login_url = "accounts:login"
