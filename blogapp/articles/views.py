from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, resolve
from django.utils import timezone
from django.views import View
from django.views.generic import FormView, UpdateView, ListView

from articles.forms import ArticleForm
from articles.models import Article, APPROVED, REJECTED, IN_PROGRESS


class AjaxView(View):
    """Required the request to be ajax"""

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax:
            messages.error(request, "Not a ajax request")
            return HttpResponseRedirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)


class EditorRequiredView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if not getattr(request.user, "is_editor", False):
            messages.error(request, "You are not an editor")
            return HttpResponseRedirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(reverse('dashboard'))


class ApprovalMixin(EditorRequiredView, PermissionRequiredMixin):
    """Requires that the user is authenticated, has the 'approve/reject'
        permission and is an editor"""
    permission_required = 'articles.approve/reject'
    permission_denied_message = \
        "You do not have the permission to approve/reject articles"

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(reverse('dashboard'))


class AddArticleView(PermissionRequiredMixin, LoginRequiredMixin, FormView):
    """Article creation FormView"""
    permission_required = 'articles.create'
    permission_denied_message = "You do not have the permission to add articles"
    template_name = 'articles/add.html'
    form_class = ArticleForm
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        article = form.save(commit=False)
        article.written_by = request.user
        article.save()
        messages.success(request, "Article added.")
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(reverse('dashboard'))


class EditArticleView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    """Article UpdateView"""
    permission_required = 'articles.edit'
    permission_denied_message = \
        "You do not have the permission to edit articles"
    template_name = 'articles/edit.html'
    model = Article
    form_class = ArticleForm
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        article = form.save(commit=False)
        article.edited_by = request.user
        article.save()
        messages.success(request, "Article edited.")
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(reverse('dashboard'))


class ArticleApprovalView(ApprovalMixin, ListView):
    """Returns list of all 'IN_PROGRESS'
        (neither approved or rejected) articles."""
    template_name = 'articles/approval.html'
    model = Article

    def get_queryset(self):
        return Article.objects.filter(status=IN_PROGRESS).order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class EditedArticlesView(EditorRequiredView, ListView):
    """Returns list of all edited articles."""
    template_name = 'articles/edited.html'
    model = Article

    def get_queryset(self):
        return Article.objects.filter(
            edited_by=self.request.user).order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ArticleStatusView(ApprovalMixin, AjaxView):
    """Approve or reject article. AJAX required"""

    def post(self, request, *args, **kwargs):
        current_url = resolve(request.path_info).view_name
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        # Not the best solution. But it works for now
        if current_url == "articles:approve":
            article.status = APPROVED
            messages.success(request, "Article approved.")
        else:
            article.status = REJECTED
            messages.warning(request, "Article rejected.")
        article.save()

        return JsonResponse({})

