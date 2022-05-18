from django.urls import path

from articles.views import AddArticleView, EditArticleView, ArticleApprovalView, ArticleStatusView, EditedArticlesView

urlpatterns = [
    path('article/add/', AddArticleView.as_view(), name='add'),
    path('article/<pk>/', EditArticleView.as_view(), name='edit'),
    path('article-approval/', ArticleApprovalView.as_view(), name='approval'),
    path('articles-edited/', EditedArticlesView.as_view(), name='articles-edited'),
    path('article/<pk>/approve/', ArticleStatusView.as_view(), name='approve'),
    path('article/<pk>/reject/', ArticleStatusView.as_view(), name='reject')
]