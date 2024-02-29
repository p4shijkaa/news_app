from django import forms

from .models import NewsCategory, TagNews, News


class AddNewsForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=NewsCategory.objects.all(), empty_label='Категория не выбрана',
                                      label='Категории')

    class Meta:
        model = News
        fields = ['name', 'content', 'slug', 'image', 'category', 'is_published']


class UploadFileForm(forms.ModelForm):
    file = forms.ImageField(label='Файл')