from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddNewsForm, UploadFileForm
from .models import News, NewsCategory, TagNews, UploadFiles
from .utils import DataMixin
from django.db.models import Q


class NewsHomePage(DataMixin, ListView):
    template_name = "news/index.html"
    context_object_name = 'news'
    title = 'Главная страница'
    extra_context = {
        'name': 'Главная страница',
        'news_categories': NewsCategory.objects.all(),
        'news_tags': TagNews.objects.all(),
    }

    def get_queryset(self):
        return News.published.all()


class NewsListCategory(DataMixin, ListView):
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_queryset(self):
        return News.published.filter(category__slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = str(context['news'][0].category)
        print(category)
        return self.get_mixin_context(context, name='Категория - ' + category)


class ShowSingleNews(DataMixin, DetailView):
    model = News
    template_name = 'news/single.html'
    slug_url_kwarg = 'news_slug'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, name=context['news'].name)


class TagNewsList(ListView):
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return News.published.filter(tags__slug=self.kwargs['tags_slug'])


class AddNewsPage(DataMixin, CreateView):
    form_class = AddNewsForm
    template_name = 'news/addnewspage.html'
    extra_context = {
        'name': 'Добавление новости',
    }


class UpdateNews(DataMixin, UpdateView):
    model = News
    fields = ['name', 'content', 'image', 'category', 'is_published']
    template_name = 'news/addnewspage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'name': 'Редактирование новости',
    }


class SearchResultsView(ListView):

    context_object_name = 'news'
    template_name = 'news/index.html'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = News.objects.filter(name__icontains=query) | News.objects.filter(content__icontains=query)
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


def add_media(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'name': 'О сайте',
        'page_obj': page_obj,
    }
    return render(request, 'news/about.html', context)
