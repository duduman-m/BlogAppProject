from django import forms
from articles.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['status'].disabled = True
        self.fields['written_by'].disabled = True
        self.fields['edited_by'].disabled = True
        if not (instance and instance.pk):
            self.fields['status'].widget = forms.HiddenInput()
            self.fields['written_by'].widget = forms.HiddenInput()
            self.fields['edited_by'].widget = forms.HiddenInput()
            self.fields['written_by'].required = False
