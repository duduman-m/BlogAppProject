from django.contrib import admin
from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "get_status", "written_by",
                    "edited_by", "created_at")

    def get_status(self, obj):
        return obj.get_status_display()

    get_status.short_description = 'Status'


admin.site.register(Article, ArticleAdmin)
