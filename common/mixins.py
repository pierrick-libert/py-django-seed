"""Collection of common mixins"""

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import DeleteView

from user.models import CustomUserRole


class SuperuserAccessOnly(UserPassesTestMixin, LoginRequiredMixin, View):
    """Superuser only mixin"""

    def test_func(self) -> bool:
        """Test for superuser func"""
        if not self.request.user.id:
            return False
        return self.request.user.role == CustomUserRole.SUPERUSER


class DeleteViewMixin(DeleteView):
    """Delete mixin which does post on get"""

    def get(self, request: WSGIRequest, *args, **kwargs) -> HttpResponseRedirect:
        """Get method"""
        self.object = self.get_object()
        self.object.deleted_by = request.user
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class OrderListViewMixin(ListView):
    """Order mixin allow ordering by views in view"""

    ordering_fields: list[str] = []

    # pylint: disable=broad-exception-caught
    def get_ordering(self) -> str | None:
        """Get ordering from url"""
        try:
            return self.request.GET.get("ordering", None) or super().get_ordering()[0]
        except Exception:
            return None

    def get_context_data(self, **kwargs) -> RequestContext:
        """Attach ordering fields and order_by to context"""
        context = super().get_context_data(**kwargs)
        context["ordering_fields"] = self.ordering_fields
        context["order_by"] = self.get_ordering()
        return context


class FilterListViewMixin(ListView):
    """Filter mixin which does filter on get from url params, and attach form to view"""

    filterset_class: Any

    # pylint: disable=not-callable
    def get_queryset(self) -> models.QuerySet:
        """Get queryset update queryset with filters"""
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset, request=self.request)  # type: ignore
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs) -> RequestContext:
        """Update context with filterset"""
        context = super().get_context_data(**kwargs)
        context["filterset"] = self.filterset
        return context


# pylint: disable=too-few-public-methods, no-member
class FilterPlaceholderSetup:
    """Filter Placeholder Setup"""

    def __init__(self, *args, **kwargs):
        """Override init for placeholder"""
        super().__init__(*args, **kwargs)

        for form_field in self.form.fields:
            field = self.form.fields[form_field]
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["data-placeholder"] = field.label
