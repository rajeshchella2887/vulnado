from django.views.generic import RedirectView


# NOTE: the root page, allow
class LandingIndexView(RedirectView):
    permanent = True
    pattern_name = "accounts:login"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.pattern_name = "dashboards:index"

        return super().get(request, *args, **kwargs)
