from datetime import datetime, timedelta
from django.db.models import Count, Q
from django.views.generic import TemplateView

from users.models import Writer


class DashboardView(TemplateView):

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_30_days = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(30)
        context['object_list'] = Writer.objects.annotate(
            articles_total=Count('articles_written'),
            articles_last_30_days=Count('articles_written', filter=Q(articles_written__created_at__gt=last_30_days)))
        return context
