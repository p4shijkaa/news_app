from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsHomePage.as_view(), name='home'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('addnewspage/', views.AddNewsPage.as_view(), name='add_news_page'),
    path('category/<slug:category_slug>/', views.NewsListCategory.as_view(), name='category'),
    path('news/<slug:news_slug>/', views.ShowSingleNews.as_view(), name='news'),
    path('tags/<slug:tags_slug>/', views.TagNewsList.as_view(), name='tags'),
    path('edit/<slug:slug>/', views.UpdateNews.as_view(), name='update'),
    path('add_news/', views.add_media, name='add_news'),
]