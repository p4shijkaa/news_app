from news.models import News
from django.db.models import Q


class DataMixin:
    title = None
    extra_content = {}
    paginate_by = 2

    def __init__(self):
        if self.title:
            self.extra_content['name'] = self.title

    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context


# def q_search(query):
#     # if query.isdigit() and len(query) <= 5:
#     #     return News.objects.filter(id=int(query))
#     return News.objects.filter(content__search=query)
