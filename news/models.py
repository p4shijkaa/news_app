from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class NewsCategory(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=News.StatusPublished.PUBLISHED)


class TagNews(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tags', kwargs={'tags_slug': self.slug})


class News(models.Model):
    class StatusPublished(models.IntegerChoices):
        NOT_PUBLISHED = 0, 'Не опубликовано'
        PUBLISHED = 1, 'Опубликовано'

    name = models.CharField(max_length=256)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    image = models.ImageField(upload_to='news_images/%Y/%m/%d', default=None, blank=True, null=True)
    category = models.ForeignKey(to=NewsCategory, on_delete=models.PROTECT, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), StatusPublished.choices)),
                                       default=StatusPublished.PUBLISHED)
    tags = models.ManyToManyField(to=TagNews, blank=True, related_name='tags')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    def __str__(self):
        return f"Новость: {self.name} | Категория: {self.category.name}"

    def get_absolute_url(self):
        return reverse('news', kwargs={'news_slug': self.slug})


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads')
